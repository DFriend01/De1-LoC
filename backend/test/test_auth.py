import pytest
from flask import g, session
from de1loc import statuscodes

@pytest.mark.parametrize(('username', 'password', 'status'), ((
    ('dfriend', 'Hello', statuscodes.SUCCESS),
    ('dfriend', '', statuscodes.BADREQUEST),
    ('', 'Hello', statuscodes.BADREQUEST),
    ('dfriend', 'World', statuscodes.FORBIDDEN),
    ('dbyrne', 'Hello', statuscodes.FORBIDDEN)
)))
def test_login(client, auth, username, password, status):
    """
    Tests the endpoint <api>/auth/login
    """

    # Checks that the correct status code is returned
    response = auth.login(username, password)
    assert response.status_code == status

    with client:
        if(status == statuscodes.SUCCESS):

            # Checks that the session was created correctly
            client.get('/')
            assert username in response.json.values()
            assert g.user['username'] == username


def test_logout(client, auth):
    """
    Tests the endpoint <api>/auth/logout
    """
    username = 'dfriend'
    password = 'Hello'
    response = auth.login(username, password)
    assert response.status_code == statuscodes.SUCCESS

    with client:

        # Checks that the user information is no longer in the session
        auth.logout()
        assert 'user_id' not in session

@pytest.mark.parametrize(('username', 'password', 'user_input_code', 'status'), ((
    ('dfriend', 'Hello', '1234', statuscodes.SUCCESS),
    ('dfriend', 'Hello', '', statuscodes.BADREQUEST),
    ('dfriend', 'Hello', '42066', statuscodes.UNAUTHORIZED),
    ('billybob', 'World', '42066', statuscodes.SUCCESS),
    ('billybob', 'World', '', statuscodes.BADREQUEST),
    ('billybob', 'World', '1234', statuscodes.UNAUTHORIZED),
)))
def test_autheticate_code_logged_in(client, auth, username, password, user_input_code, status):
    """
    Tests the endpoint <api>/auth/code
    """
    response = auth.login(username, password)
    assert response.status_code == statuscodes.SUCCESS

    with client:
        client.get('/')
        response = auth.authenticate(code=user_input_code)
        assert response.status_code == status

@pytest.mark.parametrize(('user_input_code', 'status'), ((
    ('1234', statuscodes.UNAUTHORIZED),
    ('42066', statuscodes.UNAUTHORIZED),
    ('4321', statuscodes.UNAUTHORIZED),
    ('', statuscodes.UNAUTHORIZED)
)))
def test_authenticate_code_logged_out(client, auth, user_input_code, status):
    with client:
        client.get('/')
        response = auth.authenticate(code=user_input_code)
        assert response.status_code == status
