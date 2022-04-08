from flask import (
    Blueprint, g, request, jsonify
)
from . import statuscodes
from de1loc.auth import login_required
from de1loc.db import get_db

bp = Blueprint('code', __name__, url_prefix='/code')

@bp.route("/register", methods=['POST'])
@login_required
def create_code():
    """
    URL: <api>/code/register

    POST Request
    ===========
        Registers a code tied to a user in the database.

        Body Data (Key : Datatype)
        =======================
        code : string
        codename : string

        SUCCESS (200)
        =============
        The code was successfully added to the database.

        Response Data (Key : Datatype)
        ---------------------------
            username : string
            firstname : string
            lastname : string

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        Either
            1) The code already exists in the database (regardless of username).
            2) The username in the body does not exist in the database.
        
    """
    if request.method == 'POST':
        username = g.user['username']
        code = request.json['code']
        codename = request.json['codename']

        if (not code) or (not codename):
            data = {'message' : 'Missing information'}
            return jsonify(data), statuscodes.BADREQUEST
        else:
            db = get_db()
            user = db.execute (
                'SELECT id, username, firstname, lastname FROM user WHERE username = ?', (username,)
            ).fetchone()

            if user is None:
                data = {'message' : f'Cannot register code with non-existent user {username}'}
                return jsonify(data), statuscodes.FORBIDDEN
            else:
                try:
                    db.execute (
                        'INSERT INTO code (code, codename, user_id) VALUES (?, ?, ?)', (code, codename, user['id'])
                    )
                    db.commit()
                except db.IntegrityError:
                    data = {'message' : f'Cannot register duplicate codes'}
                    return jsonify(data), statuscodes.FORBIDDEN
                data = db.execute('SELECT * FROM code WHERE code = ?', (code,)).fetchone()
                return jsonify(dict(data)), statuscodes.SUCCESS

@bp.route("/modify", methods=['POST'])
@login_required
def modify_code():
    """
    URL: <api>/code/modify

    POST Request
    ===========
        Modifies a code in the database. Can change the name of the code, or the code itself.

        Body Data (Key : Datatype)
        =======================
        id : integer
        code : string
        codename : string

        SUCCESS (200)
        =============
        The code was successfully modified.

        Response Data (Key : Datatype)
        ---------------------------
            N/A

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        The username in the body does not exist in the database.

        SERVERERROR (500)
        =================
        Something went wrong updating the code.
        
    """
    if request.method == 'POST':
        username = g.user['username']
        code_id = request.json['id']
        new_code = request.json['code']
        new_codename = request.json['codename']

        if(not username) or (not code_id) or (not new_code) or (not new_codename):
            data = {'message' : 'Missing information'}
            return jsonify(data), statuscodes.BADREQUEST
        else:
            db = get_db()
            code_data = db.execute(
                'SELECT * FROM code WHERE id = ?', (code_id,)
            ).fetchone()

            if code_data is None:
                data = {'message' : 'Code id not registered'}
                return jsonify(data), statuscodes.BADREQUEST
            
            user_data = db.execute(
                'SELECT * FROM user WHERE id = ?', (code_data['user_id'],)
            ).fetchone()

            if user_data is None:
                data = {'message' : 'User does not exist'}
                return jsonify(data), statuscodes.BADREQUEST

            if username != user_data['username']:
                data = {'message' : 'Username does not match'}
                return jsonify(data), statuscodes.FORBIDDEN

            try:
                db.execute(
                    'UPDATE code SET code = ?, codename = ? WHERE id = ?', (new_code, new_codename, code_id)
                )
                db.commit()
                return jsonify({}), statuscodes.SUCCESS
            except:
                data = {'message' : 'Something went wrong'}
                return jsonify(data), statuscodes.SERVERERROR

@bp.route("/delete", methods=["DELETE"])
@login_required
def delete_code():
    """
    URL: <api>/code/delete

    DELETE Request
    ===========
        Deletes a code from the database.

        Body Data (Key : Datatype)
        =======================
        id : integer

        SUCCESS (200)
        =============
        The code was successfully deleted.

        Response Data (Key : Datatype)
        ---------------------------
            N/A

        BAD REQUEST (400)
        =================
        Information is missing in the body.

        UNAUTHORIZED (401)
        ==================
        The user is not logged in.

        FORBIDDEN (403)
        ===============
        The username in the body does not exist in the database.

        SERVERERROR (500)
        =================
        Something went wrong deleting the code.
        
    """
    if request.method == "DELETE":
        username = g.user['username']
        code_id = request.json['id']

        if(not username) or (not code_id):
            data = {'message' : 'Missing information'}
            return jsonify(data), statuscodes.BADREQUEST
        else:
            db = get_db()

            code_data = db.execute(
                'SELECT * FROM code WHERE id = ?', (code_id,)
            ).fetchone()

            if code_data is None:
                data = {'message' : 'Code id not registered'}
                return jsonify(data), statuscodes.BADREQUEST
            
            user_data = db.execute(
                'SELECT * FROM user WHERE id = ?', (code_data['user_id'],)
            ).fetchone()

            if user_data is None:
                data = {'message' : 'User does not exist'}
                return jsonify(data), statuscodes.BADREQUEST

            if username != user_data['username']:
                data = {'message' : 'Username does not match'}
                return jsonify(data), statuscodes.FORBIDDEN

            try:
                db.execute(
                    'DELETE FROM code WHERE id = ?', (code_id,)
                )
                db.commit()
                return jsonify({}), statuscodes.SUCCESS
            except:
                data = {'message' : 'Something went wrong'}
                return jsonify(data), statuscodes.SERVERERROR


@bp.route("/test", methods=['GET'])
def get_code_table():
    db = get_db()
    try:
        codes = db.execute (
            'SELECT * FROM code', ()
        ).fetchall()
        
        codes_dict = {}
        for i, row in enumerate(codes):
            codes_dict[i] = dict(row)

        return jsonify(codes_dict), statuscodes.SUCCESS
    except:
        data = {'message' : 'Something went wrong fetching the database'}
        return jsonify(data), statuscodes.SERVERERROR
