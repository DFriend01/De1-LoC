import pytest
from de1loc import statuscodes
from de1loc.db import get_db
from werkzeug.security import check_password_hash

@pytest.mark.parametrize(('username', 'firstname', 'lastname', 'password', 'status'), ((
    ('dbyrne', 'Declan', 'Byrne', 'World', statuscodes.SUCCESS),
    ('hpatel', 'Harshil', 'Patel', 'I_Skip_Math_307', statuscodes.SUCCESS)
)))
def test_successful_register(client, user, username, firstname, lastname, password, status):
    """
    Tests the endpoint <api>/user/register. Specifically tests for status code 200.
    """

    # Check if the correct status code is returned
    response = user.register(username, firstname, lastname, password)
    assert response.status_code == status

    with client:
        # Check that the response contains the correct information
        client.get('/')
        assert username in response.json.values()

        # Check that the user was registered in the database correctly
        db = get_db()
        user_db = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        assert user_db is not None
        assert user_db['username'] == username
        assert user_db['firstname'] == firstname
        assert user_db['lastname'] == lastname
        assert user_db['face_enabled'] == 0
        assert check_password_hash(user_db['password'], password)

@pytest.mark.parametrize(('username', 'firstname', 'lastname', 'password', 'status'), ((
    ('new_user', 'new', 'user', '', statuscodes.BADREQUEST),
    ('new_user', 'new', '', 'dsfasf', statuscodes.BADREQUEST),
    ('new_user', '', 'user', 'asdfasdf', statuscodes.BADREQUEST),
    ('', 'new', 'user', 'asdfasdfsadf', statuscodes.BADREQUEST)
)))
def test_badrequest_register(user, username, firstname, lastname, password, status):
    """
    Tests the endpoint <api>/user/register. Specifically tests for status code 400.
    """

    # Check if the correct status code is returned
    response = user.register(username, firstname, lastname, password)
    assert response.status_code == status

@pytest.mark.parametrize(('username', 'status'), ((
    ('dbyrne', statuscodes.FORBIDDEN),
    ('hpatel', statuscodes.FORBIDDEN)
)))
def test_forbidden_register(user, username, status):
    """
    Tests the endpoint <api>/user/register. Specifically tests for status code 403.
    """

    # Add usernames to the database
    res1 = user.register(username, 'First1', 'Last1', 'password1')
    assert res1.status_code == statuscodes.SUCCESS

    # Return FORBIDDEN for a duplicate username
    res2 = user.register(username, 'Frist1', 'Last2', 'password2')
    assert res2.status_code == status

def test_user_profile_logged_in(client, auth, user):
    """
    Tests the endpoint <api>/user/profile when the user is logged in.
    """

    # The user logs in
    username = 'dfriend'
    password = 'Hello'
    response = auth.login(username, password)

    assert response.status_code == statuscodes.SUCCESS
    assert response.json['username'] == username

    # Check that the profile is fetch correctly
    profile = user.get_profile()
    assert profile.status_code == statuscodes.SUCCESS

    with client:
        client.get('/')
        db = get_db()
        user_db = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        assert profile.json['username'] == user_db['username']
        assert profile.json['firstname'] == user_db['firstname']
        assert profile.json['lastname'] == user_db['lastname']
        assert profile.json['face_enabled'] == user_db['face_enabled']

def test_user_profile_logged_out(user):
    """
    Tests the endpoint <api>/user/profile when the user is logged in.
    """
    profile = user.get_profile()
    assert profile.status_code == statuscodes.UNAUTHORIZED

def test_user_codes_logged_in(user, auth, code):
    """
    Tests the endpoint <api>/user/codes when the user is logged in.
    """
    # The user logs in
    username = 'dfriend'
    password = 'Hello'
    firstcode = '1234'
    response = auth.login(username, password)

    assert response.status_code == statuscodes.SUCCESS
    assert response.json['username'] == username

    # Check that the code was registered into the database
    new_code = '4321'
    codename = 'Test Code'
    response = code.create(new_code, codename)
    assert response.status_code == statuscodes.SUCCESS

    codes = user.get_codes()
    assert codes.status_code == statuscodes.SUCCESS

    firstcode_found = False
    new_code_found = False
    for _, data in codes.json.items():
        if firstcode in data.values():
            firstcode_found = True
        if (new_code in data.values()) and (codename in data.values()):
            new_code_found = True
    
    assert firstcode_found and new_code_found

def test_user_codes_logged_out(user):
    """
    Tests the endpoint <api>/user/codes when the user is logged out.
    """
    response = user.get_codes()
    assert response.status_code == statuscodes.UNAUTHORIZED    
