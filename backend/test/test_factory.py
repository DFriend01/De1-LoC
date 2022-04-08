from de1loc import create_app

# https://flask.palletsprojects.com/en/2.0.x/tutorial/tests/
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
    