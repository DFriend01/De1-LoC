from flask import (
    Blueprint, g, request, jsonify
)
from . import statuscodes
from werkzeug.security import generate_password_hash
from de1loc.db import get_db
from de1loc.auth import login_required
from .FacialClassifier.embeddings import compute_embeddings
from .FacialClassifier.model_train import trainModel
from PIL import Image
import io
import numpy as np
import threading

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route("/register", methods=['POST'])
def create_user():
    """
    URL: <api>/user/register

    POST Request
    ===========
        Registers a user in the database.

        Body Data (Key : Datatype)
        =======================
        username : string
        firstname : string
        lastname : string
        password : string

        SUCCESS (200)
        =============
        The user was successfully added to the database.

        Response Data (Key : Datatype)
        ---------------------------
            username : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        FORBIDDEN (403)
        ===============
        The username already exists in the database.

    """
    if request.method == "POST":
        username = request.json['username']
        firstname = request.json['firstname']
        lastname = request.json['lastname']
        password = request.json['password']
        face_enabled = 0

        if (not username) or (not firstname) or (not lastname) or (not password):
            data = {'message' : 'Missing information'}
            return jsonify(data), statuscodes.BADREQUEST
        else:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, firstname, lastname, password, face_enabled) VALUES (?, ?, ?, ?, ?)",
                    (username, firstname, lastname, generate_password_hash(password), face_enabled)
                )
                db.commit()
            except db.IntegrityError:
                data = {'message' : f'User {username} already exists'}
                return jsonify(data), statuscodes.FORBIDDEN
            return jsonify({"username" : username}), statuscodes.SUCCESS

@bp.route("/profile", methods=['GET'])
@login_required
def get_user_profile():
    """
    URL: <api>/user/profile

    GET Request
    ===========
        Gets the information of the currently logged in user.

        SUCCESS (200)
        =============
        The user's information was successfully fetched.

        Response Data (Key : Datatype)
        ------------------------------
            username : string
            firstname : string
            lastname : string
            face_enabled : boolean (0 or 1)

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

    """

    if request.method == 'GET':
        db = get_db()
        user_data = db.execute(
            'SELECT username, firstname, lastname, face_enabled FROM user WHERE id = ?',
            (g.user['id'],)
        ).fetchone()
        user_data = dict(user_data)
        return jsonify(user_data), statuscodes.SUCCESS

@bp.route("/codes", methods=['GET'])
@login_required
def get_user_codes():
    """
    URL: <api>/user/codes

    GET Request
    ===========
        Gets the codes corresponding to the currently logged in user.

        SUCCESS (200)
        =============
        The user's codes were successfully fetched.

        Response Data (Key : Datatype)
        ------------------------------
            (A number) : dictionary

            dictionary data
                id : integer
                code : string
                codename : string
                user_id : integer

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        SERVERERROR (500)
        =================
        Something went wrong fetching the codes.

    """
    if request.method == 'GET':
        user_id = g.user['id']
        db = get_db()

        try:
            codes = db.execute (
                'SELECT * FROM code WHERE user_id = ?', (user_id,)
            ).fetchall()

            codes_dict = {}
            for i, row in enumerate(codes):
                codes_dict[i] = dict(row)

            return jsonify(codes_dict), statuscodes.SUCCESS

        except:
            data = {'message' : 'Something went wrong fetching the database'}
            return jsonify(data), statuscodes.SERVERERROR

# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def getImage(fileObj):
    image_data = fileObj.read()
    image = Image.open(io.BytesIO(image_data))
    image = image.transpose(Image.ROTATE_270)

    # Convert PIL image to opencv format
    # https://stackoverflow.com/questions/14134892/convert-image-from-pil-to-opencv-format
    image = image.convert('RGB')
    image = np.array(image)
    image = image[:, :, ::-1].copy() 
    return image

@bp.route('/reguserface', methods=['POST'])
@login_required
def enable_face_recognition():
    """
    URL: <api>/user/reguserface

    POST Request
    ===========
        Given multiple photos, register a user with facial recognition.

        Body Data (Key : Datatype)
        =======================
        p1 : file (.png, .jpg, .jpeg)
        p2 : file (.png, .jpg, .jpeg)
        .
        .
        .

        SUCCESS (200)
        =============
        The user was successfully registered with facial recognition.

        BAD REQUEST (400)
        =================
        Either no photos have not been provided, or the file provided is not a photo.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        The user has already enabled facial recognition.
        
    """
    if request.method == 'POST':
        db = get_db()
        user_id = g.user['id']

        # Reject the request if the user already has face detection enabled
        user_db = db.execute(
            "SELECT face_enabled FROM user WHERE id = ?",
            (user_id,)
        ).fetchone()
        if user_db['face_enabled']:
            return jsonify({'message' : 'Facial recognition already activated for this user'}), statuscodes.FORBIDDEN

        # Check if at least one file has been sent
        if len(request.files) == 0:
            return jsonify({'message' : 'No files submitted'}), statuscodes.BADREQUEST

        # Check that all the files are photos
        for _, file in request.files.items():
            if not allowed_file(file.filename):
                return jsonify({'message' : 'One of the files submitted is not a photo'}), statuscodes.BADREQUEST

        # Compute embeddings and save them
        for _, file in request.files.items():
            image = getImage(file)
            compute_embeddings(image, user_id)

        # Update boolean in user table to have face detection enabled
        db.execute(
            "UPDATE user SET face_enabled = 1 WHERE id = ?",
            (user_id,)
        )
        db.commit()

        # Fork a process to train the new model in the background
        t = threading.Thread(target=trainModel, name='classifier_training')
        t.start()
        
        return jsonify({}), statuscodes.SUCCESS

@bp.route("/test", methods=['GET'])
def get_user_table():
    db = get_db()
    try:
        users = db.execute (
            'SELECT * FROM user'
        ).fetchall()

        users_dict = {}
        for i, row in enumerate(users):
            users_dict[i] = dict(row)

        return jsonify(users_dict), statuscodes.SUCCESS
    except:
        data = {'message' : 'Something went wrong fetching the database'}
        return jsonify(data), statuscodes.SERVERERROR
