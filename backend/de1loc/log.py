from flask import (
    Blueprint, request, jsonify
)
from . import statuscodes
from de1loc.db import get_db
from datetime import datetime
from pytz import timezone
import pytz

bp = Blueprint('log', __name__, url_prefix='/log')

INVALID_USER_ID = -1
INVALID_USERNAME = "N/A"
INVALID_CODENAME = "N/A"
NLOGS = 50
NO_OFFSET = 0

def log(user_id=INVALID_USER_ID, username=INVALID_USERNAME, codename=INVALID_CODENAME, success=False):
    db = get_db()
    success_int = 1 if success else 0

    # Get current date in PST
    currdate = datetime.now(tz=pytz.utc)
    currdate = currdate.astimezone(timezone('US/Pacific'))

    if user_id == INVALID_USER_ID:
        db.execute(
            'INSERT INTO log (user_id, username, codename, verifDate, verifTime, success) VALUES (NULL, ?, ?, ?, ?, ?)',
            (INVALID_USERNAME, INVALID_CODENAME, currdate.strftime("%Y-%m-%d"), currdate.strftime("%H:%M:%S"), success_int)
        )
    else:   
        db.execute(
            'INSERT INTO log (user_id, username, codename, verifDate, verifTime, success) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, username, codename, currdate.strftime("%Y-%m-%d"), currdate.strftime("%H:%M:%S"), success_int)
        )
    db.commit()

    return currdate

def query(username, nlogs, offset):
    db = get_db()
    if username:
        user_id = db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user_id:
            user_id = user_id['id']
            return db.execute(
                'SELECT user_id, username, codename, verifDate, verifTime, success FROM log ' +\
                'WHERE user_id = ? ' +\
                'ORDER BY verifDate DESC, verifTime DESC ' +\
                'LIMIT ? OFFSET ?',
                (user_id, nlogs, offset)
            ).fetchall()
        else:
            return None
    else:
        return db.execute(
            'SELECT user_id, username, codename, verifDate, verifTime, success FROM log ' +\
            'ORDER BY verifDate DESC, verifTime DESC ' +\
            'LIMIT ? OFFSET ?',
            (nlogs, offset)
        ).fetchall()

@bp.route('/query', methods=['GET'])
def queryLog():
    """
    URL: <api>/log/query?user=value1&nlogs=value2&offset=value3

    GET Request
    ===========
        Gets the most recent activity specified by nlogs. All of "user", "nlogs", and "offset" are optional
        parameters to the query string.

        Query Data (name : datatype)
        ----------------------------
        user : string (optional)
            The username of the user to be queried. If not specified, then the username is not
            considered in the query.

        nlogs : int (optional)
            The number of entries returned by the query. Note that the "nlogs" most recent entries
            are returned. If not specified, then the 50 most recent logs are returned.

        offset : int (optional)
            The offset of where to start querying. For example, if offset was 5, then the "nlogs" most recent
            entries starting at the 5th entry are returned. If not specified, then the offset is 0.

        SUCCESS (200)
        =============
            The query was successful. Note that the response data is sorted by date and then by time
            in descending order (most recent to least recent).

            Response Data (Key : Datatype)
            ------------------------------
            (A number) : Dictionary

            Dictionary Data
                user_id : int
                username : string
                codename : string
                verifDate : string  ("YYYY-MM-DD")
                verifTime : string  ("HH:MM:SS")
                success : int       (0 or 1)
    """
    if request.method == 'GET':
        args = request.args
        
        try:
            nlogs = int(args['nlogs'])
        except:
            nlogs = NLOGS

        try:
            username = str(args['user'])
        except:
            username = None

        try:
            offset = int(args['offset'])
        except:
            offset = NO_OFFSET

        db = get_db()
        logs = query(username, nlogs, offset)

        logs_dict = {}
        if logs:
            logs_dict = {}
            for i, row in enumerate(logs):
                logs_dict[i] = dict(row)
                logs_dict[i]['verifDate'] = logs_dict[i]['verifDate'].strftime("%Y-%m-%d")

        return jsonify(logs_dict), statuscodes.SUCCESS
