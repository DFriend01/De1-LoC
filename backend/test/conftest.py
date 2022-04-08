import os
import tempfile
import pytest
import sys

# https://flask.palletsprojects.com/en/2.0.x/tutorial/tests/

# Add python directory to path
testdir = os.path.dirname(__file__)
srcdir = "../"
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

from de1loc import create_app
from de1loc.db import init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    """
    Invoke HTTP authentication requests.
    """
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        """
        Request for <api>/auth/login
        """
        return self._client.post(
            '/auth/login',
            json={'username': username, 'password': password}
        )

    def logout(self):
        """
        Request for <api>/auth/logout
        """
        return self._client.post('/auth/logout')

    def authenticate(self, code='1234'):
        """
        Request for <api>/auth/code
        """
        return self._client.post(
            '/auth/code',
            json={'code' : code}
        )

@pytest.fixture
def auth(client):
    """
    Returns an instance of AuthActions.
    """
    return AuthActions(client)


class UserActions(object):
    """
    Invoke HTTP user requests on <api>/user.
    """
    def __init__(self, client):
        self._client = client

    def register(self, username, firstname, lastname, password):
        """
        Request for <api>/code/register
        """
        return self._client.post(
            '/user/register',
            json={'username' : username, 'password' : password, 'firstname' : firstname, 'lastname' : lastname}
        )

    def get_profile(self):
        """
        Request for <api>/user/profile
        """
        return self._client.get('/user/profile')

    def get_codes(self):
        """
        Request for <api>/user/codes
        """
        return self._client.get('/user/codes')

@pytest.fixture
def user(client):
    """
    Returns an instance of UserActions.
    """
    return UserActions(client)


class CodeActions(object):
    """
    Invoke HTTP code requests on <api>/code.
    """
    def __init__(self, client):
        self._client = client

    def create(self, code, codename):
        """
        Request on <api>/code/register
        """
        return self._client.post(
            '/code/register',
            json={'code' : code, 'codename' : codename}
        )

    def modify(self, id, code, codename):
        """
        Request for <api>/code/modify
        """
        return self._client.post(
            '/code/modify',
            json={'id' : id, 'code' : code, 'codename' : codename}
        )

    def delete(self, id):
        """
        Request for <api>/code/delete
        """
        return self._client.delete(
            '/code/delete',
            json={'id' : id}
        )

@pytest.fixture
def code(client):
    """
    Returns an instance of CodeActions
    """
    return CodeActions(client)

class LogActions(object):
    """
    Invoke HTTP requests on <api>/log
    """
    def __init__(self, client):
        self._client = client

    def query(self, username=None, nlogs=None, offset=None):
        url = '/log/query'
        params = {'user' : username, 'nlogs' : nlogs, 'offset' : offset}
        params_added = False

        for name, value in params.items():
            if value is not None:
                if not params_added:
                    url += "?" + name + "=" + str(value)
                    params_added = True
                else:
                    url += "&" + name + "=" + str(value)
        
        return self._client.get(url)

@pytest.fixture
def log(client):
    """
    Returns an instance of LogActions
    """
    return LogActions(client)
