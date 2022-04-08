import functools
import numpy as np
from firebase_admin import messaging
from flask import (
    Blueprint, g, request, session, jsonify
)
from . import statuscodes
from werkzeug.security import check_password_hash
from de1loc.db import get_db
from de1loc.log import log
from datetime import datetime
from pytz import timezone
import pytz
from PIL import Image
import io

from .FacialClassifier.model_eval import evalModel
from .OutlierDetection.model.OutlierDetection import OutlierDetection
from .log import query

TIMEOUT_INTERVAL = 5 * 60 # 5 minutes in seconds
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
AUTHTIME = datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
AUTHENTICATED = False

bp = Blueprint('auth', __name__, url_prefix='/auth')

def timeStringToNumpy(datestr=None, timestr=None, date=None):
    """
    Converts either a datetime object or strings representing the date and time
    to a numpy array where the first entry is the day of the week, and the
    second entry is the time represented as a continuous value.

    Arguments
    ---------
    str : datestr
        The date string formatted as YYYY-MM-DD

    str : timestr
        The time string formatted as HH:MM:SS

    datetime : date
        The date as a datetime object

    Returns
    -------
    np.array
        A numpy array where the first entry is the day of the week, and the
        second entry is the time represented as a continuous value.
    """
    
    if date is None:
        timestr = f"{datestr} {timestr}"
        dateobj = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')

        day = float(dateobj.weekday())
        hour = dateobj.hour
        minute = dateobj.minute
        sec = dateobj.second
        time = hour + (minute / 60) + (sec / 3600)
        return np.array([time, day])
    else:
        day = float(date.weekday())
        hour = date.hour
        minute = date.minute
        sec = date.second
        time = hour + (minute / 60) + (sec / 3600)
        return np.array([[time, day]])

def detect_outliers(user_id, username, codename):
    """
    Detects if the most recent unlock was an outlier compared to the most recent data
    of a user.

    Arguments
    ---------
    int : user_id
        The id of the user stored in the database.

    str : username
        The username of the user.

    str : codename
        The codename of the code used to unlock. If facial recognition was used, then
        the codename should be 'face'.

    Returns
    -------
    bool
        Returns True if the latest unlock was an outlier, and False otherwise.
    """
    currdate = datetime.now()
    db = get_db()
    data = db.execute(
        "SELECT * FROM log " +\
        "WHERE user_id = ? AND success = 1 " +\
        "ORDER BY verifDate DESC, verifTime DESC " +\
        "LIMIT 100",
        (user_id,)
    ).fetchall()

    data_array = []
    currdate = timeStringToNumpy(date=currdate)
    for row in data:
        data_array.append(timeStringToNumpy(row['verifDate'], row['verifTime']))
    data_array = np.array(data_array)

    if data_array.size > 0:
        outlier_detector = OutlierDetection(num_neighbors=5, max_ratio=1.5, min_data_len=10, max_data_len=100, initial_data=data_array)
        isoutlier = outlier_detector.add(currdate, debug=True)

        if isoutlier and ('token' in session):
            # https://firebase.google.com/docs/admin/setup#python
            registration_token = session['token']
            message = messaging.Message(
                data={
                    'username' : username,
                    'codename' : codename
                },
                android=messaging.AndroidConfig(
                    notification=None
                ),
                token=registration_token,
            )
            response = messaging.send(message)
            print('Successfully sent message:', response)
        else:
            print("Not an Outlier!")


def login_required(view):
    """
    Middleware for authentication.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return jsonify({'message' : 'Login required'}), statuscodes.UNAUTHORIZED
        return view(**kwargs)
    return wrapped_view

@bp.route('/code', methods=['POST'])
@login_required
def authenticate_code():
    """
    URL: <api>/auth/code

    POST Request
    ===========
        Given a username and a code, the information is verified against the data stored in the database
        and responds accordingly.

        Body Data (Key : Datatype)
        =======================
        code : string

        SUCCESS (200)
        =============
        The username matches the code given and authentication was successful.

        Response Data (Key : Datatype)
        ---------------------------
            username : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The code in the body is not registered with the username, or the user is not logged in.
            
    """
    global AUTHENTICATED
    global AUTHTIME
    
    if request.method == 'POST':
        code = request.json['code']

        if not code:
            data = {'message' : 'Missing information'}
            return jsonify(data), statuscodes.BADREQUEST
        else:
            db = get_db()

            code_db = db.execute (
                'SELECT user_id, codename FROM code WHERE code.code = ?', (code,)
            ).fetchone()

            if (code_db is None) or (g.user['id'] != code_db['user_id']):
                detect_outliers(g.user['id'], g.user['username'], "N/A")
                log(user_id=g.user['id'], username=g.user['username'], success=False) # Log an unsuccessful unlock attempt
                data = {'message' : f'Code is not registered with user {g.user["username"]}'}
                return jsonify(data), statuscodes.UNAUTHORIZED
            else:
                detect_outliers(g.user['id'], g.user['username'], code_db['codename'])
                log(user_id=g.user['id'], username=g.user['username'], codename=code_db['codename'], success=True) # Log a successful unlock attempt
                data = {'username' : g.user['username']}
                AUTHENTICATED = True
                AUTHTIME = datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
                return jsonify(data), statuscodes.SUCCESS

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
def allowed_file(filename):
    """
    Checks if a filename has a valid extension
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getImage(fileObj):
    """
    Extracts an image from a file object received in a POST request.
    """
    image_data = fileObj.read()
    image = Image.open(io.BytesIO(image_data))
    #image = image.transpose(Image.ROTATE_270)

        # Convert PIL image to opencv format
        # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    image = image.convert('RGB')
    image = np.array(image)
    image = image[:, :, ::-1].copy()
    # image_data = fileObj.read()
    # image = Image.open(io.BytesIO(image_data))
    # image = image.transpose(Image.ROTATE_270)

    # # Convert PIL image to opencv format
    # # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    # image = image.convert('RGB')
    # image = np.array(image)
    # image = image[:, :, ::-1].copy() 
    return image

@bp.route('/face', methods=['POST'])
@login_required
def authenticate_face():
    """
    URL: <api>/auth/face

    POST Request
    ===========
        Given a photo, verify the user against the facial recognition model to unlock the lock.

        Body Data (Key : Datatype)
        =======================
        file : file (.png, .jpg, .jpeg)

        SUCCESS (200)
        =============
        The face in the photo matches the embeddings trained in the facial recognition model.

        BAD REQUEST (400)
        =================
        Either exactly one photo has not been provided, or the file provided is not a photo.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        Either the user does not have facial recognition enabled, or the face submitted to the model
        does not match the user's facial embeddings.
    """
    if request.method == "POST":
        db = get_db()
        user_id = g.user['id']

        ############################################################
        # DECLAN
        """
        import cv2 as cv
        file = request.files['file']
        assert allowed_file(file.filename)

        # This funtion applies the rotation. If the output is not oriented as desired, try the code labelled with "ALTERNATIVE"
        image = getImage(file)
        """

        # ALTERNATIVE (Image unrotated)
        """
        image_data = file.read()
        image = Image.open(io.BytesIO(image_data))

        # Convert PIL image to opencv format
        # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
        image = image.convert('RGB')
        image = np.array(image)
        image = image[:, :, ::-1].copy() 
        """

        # Show the image and return early
        """
        cv.imshow('Image Window', image)
        cv.waitKey(0)
        cv.destroyAllWindows() 
        return jsonify({}), 200
        """

        ############################################################

        global AUTHENTICATED
        global AUTHTIME

        # Reject the request if the user does not have face detection enabled
        user_db = db.execute(
            "SELECT face_enabled FROM user WHERE id = ?",
            (user_id,)
        ).fetchone()
        if not user_db['face_enabled']:
            return jsonify({'message' : 'Facial recognition already activated for this user'}), statuscodes.FORBIDDEN

        # Check if one photo has been sent
        if len(request.files) != 1:
            return jsonify({'message' : 'Must submit exactly 1 photo'}), statuscodes.BADREQUEST

        # Get the file and see if the filename is legal
        file = request.files['file']
        if not allowed_file(file.filename):
            return jsonify({'message' : 'One of the files submitted is not a photo'}), statuscodes.BADREQUEST
        image = getImage(file)

        unlock = evalModel(image, g.user['id'])

        if not unlock:
            log(user_id=g.user['id'], username=g.user['username'], success=0)
            AUTHENTICATED = False
            return jsonify({'message' : 'Unauthorized face'}), statuscodes.FORBIDDEN
        else:
            detect_outliers(g.user['id'], g.user['username'], "Face")
            log(user_id=g.user['id'], username=g.user['username'], codename="Face", success=1)
            AUTHENTICATED = True
            AUTHTIME = datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
            return jsonify({}), statuscodes.SUCCESS
            

@bp.before_app_request
def load_logged_in_user():
    """
    Loads in user id from the cookie before each page loads

    """
    global AUTHENTICATED
    global AUTHTIME

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        # Timeout an app unlock request
        curtime = datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
        delta = curtime - AUTHTIME
        if delta.total_seconds() > TIMEOUT_INTERVAL:
            AUTHTIME = datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
            AUTHENTICATED = False


@bp.route("/login", methods=["POST"])
def login():
    """
    URL: <api>/auth/login

    POST Request
    ============
        Given a username and a password, a user is logged in if the credentials are correct.
        The user id is loaded into a cookie until the user logs out.

        Body Data (Key : Datatype)
        ==========================
        username : string
        password : string
        token : string

        SUCCESS (200)
        =============
        The login credentials are correct and authentication was successful.

        Response Data (Key : Datatype)
        ---------------------------
            username : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        FORBIDDEN (403)
        ===============
        The login credentials are incorrect.

    """
    global AUTHENTICATED
    global AUTHTIME

    if request.method == "POST":
        username = request.json['username']
        password = request.json['password']
        token = request.json['token']

        if(not username) or (not password) or (not token):
            data = {'message' : 'Incorrect username or password'}
            return jsonify(data), statuscodes.BADREQUEST

        db = get_db()
        user_data = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if (user_data is None) or (not check_password_hash(user_data['password'], password)):
            data = {'message' : 'Incorrect username or password'}
            return jsonify(data), statuscodes.FORBIDDEN
        else:
            session.clear()
            session['user_id'] = user_data['id']
            session['token'] = token
            AUTHENTICATED = False
            AUTHTIME = datetime.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
            return jsonify({'username' : user_data['username']}), statuscodes.SUCCESS

@bp.route('/logout', methods=["POST"])
def logout():
    """
    URL: <api>/auth/login

    POST Request
    ============
        The currently logged in user is logged out and the session is cleared.

        SUCCESS (200)
        =============
        The login credentials are correct and authentication was successful.

    """
    global AUTHENTICATED
    if request.method == "POST":
        session.clear()
        AUTHENTICATED = False
        return jsonify({'message' : 'Logout successful'}), statuscodes.SUCCESS

@bp.route('/verify/pinpad', methods=['POST'])
def verify_pinpad():
    if request.method == 'POST':
        n1 = None
        n2 = None
        n3 = None
        n4 = None
        try:
            n1 = str(request.json['msg']['num1'])
            n2 = str(request.json['msg']['num2'])
            n3 = str(request.json['msg']['num3'])
            n4 = str(request.json['msg']['num4'])
            assert (n1 and n2 and n3 and n4)
        except:
            return jsonify({'message' : 'Invalid 4 digit code'}), statuscodes.BADREQUEST

        input_code = n1 + n2 + n3 + n4

        db = get_db()
        code_db = db.execute (
            'SELECT user_id, codename FROM code WHERE code.code = ?', (input_code,)
        ).fetchone()

        if (code_db is None):
            log(user_id=0, username="N/A", success=False) # Log an unsuccessful unlock attempt
            data = {'message' : f'Code is not registered'}
            return jsonify(data), statuscodes.UNAUTHORIZED
        else:
            user_db = db.execute(
                'SELECT username FROM user WHERE id = ?', (code_db['user_id'],)
            ).fetchone()
            detect_outliers(code_db['user_id'], user_db['username'], code_db['codename'])
            log(user_id=code_db['user_id'], username=user_db['username'], codename=code_db['codename'], success=True) # Log a successful unlock attempt
            data = {'username' : user_db['username']}
            return jsonify(data), statuscodes.SUCCESS

@bp.route('/verify/app', methods=['GET'])
def verify_app():
    global AUTHENTICATED

    if request.method == 'GET':
        try:
            authenticated = AUTHENTICATED
            print(authenticated)
            if authenticated:
                AUTHENTICATED = False
                return jsonify({}), statuscodes.SUCCESS
            else:
                AUTHENTICATED = False
                return jsonify({}), statuscodes.UNAUTHORIZED
        except:
            AUTHENTICATED = False
            return jsonify({}), statuscodes.UNAUTHORIZED
