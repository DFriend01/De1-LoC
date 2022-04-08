import pytest
from de1loc import statuscodes
from de1loc.db import get_db

def test_create_code_logged_in(auth, code):
    """
    Testing the endpoint <api>/code/register for status 200.
    """
    # Login user
    username = 'dfriend'
    password = 'Hello'
    response = auth.login(username, password)
    assert response.status_code == statuscodes.SUCCESS

    # Create a new code
    new_code = '52312'
    codename = 'My Code'
    response = code.create(new_code, codename)
    assert response.status_code == statuscodes.SUCCESS
    assert response.json['code'] == new_code
    assert response.json['codename'] == codename

    # Check that the user can authenticate the lock with their new code
    response = auth.authenticate(code=new_code)
    assert response.status_code == statuscodes.SUCCESS

def test_create_code_logged_out(code):
    """
    Testing the endpoint <api>/code/register for status 401.
    """
    # Create a new code
    new_code = '52312'
    codename = 'My Code'
    response = code.create(new_code, codename)
    assert response.status_code == statuscodes.UNAUTHORIZED
