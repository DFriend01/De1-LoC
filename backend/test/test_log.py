import pytest
from de1loc import statuscodes
from de1loc.db import get_db
from datetime import date
from datetime import datetime

NO_USER = -1

@pytest.mark.parametrize(('user_id', 'username', 'password', 'user_input', 'codename', 'success', 'authstatus'), ((
    (1, 'dfriend', 'Hello', '1234', 'Default', 1, statuscodes.SUCCESS),
    (1, 'dfriend', 'Hello', '42066', "N/A", 0, statuscodes.UNAUTHORIZED),
    (1, 'dfriend', 'Hello', '992934', "N/A", 0, statuscodes.UNAUTHORIZED),
    (2, 'billybob', 'World', '42066', "Bob's Code", 1, statuscodes.SUCCESS),
    (2, 'billybob', 'World', '1234', "N/A", 0, statuscodes.UNAUTHORIZED),
    (2, 'billybob', 'World', '27392', "N/A", 0, statuscodes.UNAUTHORIZED),
)))
def test_successful_logging(client, auth, user_id, username, password, user_input, codename, success, authstatus):
    """
    Tests the logging mechanism when logged in users unlock the door
    """

    # Get the date
    today = date.today()
    datestr = today.strftime("%Y-%m-%d")

    # Checks that the correct status code is returned
    response = auth.login(username, password)
    assert response.status_code == statuscodes.SUCCESS

    # Lock authentication
    response = auth.authenticate(code=user_input)
    assert response.status_code == authstatus

    with client:
        client.get('/')
        db = get_db()
        data = db.execute('SELECT * FROM log WHERE user_id = ? ORDER BY verifDate DESC, verifTime DESC', (user_id,)).fetchall()
        assert data is not None
        assert data[0]['user_id'] == user_id
        assert data[0]['username'] == username
        assert data[0]['codename'] == codename
        assert data[0]['verifDate'].strftime("%Y-%m-%d") == datestr
        assert data[0]['success'] == success

@pytest.mark.parametrize(('user_id', 'username', 'nlogs', 'offset', 'expected_nlogs'), ((
    (NO_USER, None, 14, None, 14),
    (NO_USER, None, 10, 0, 10),
    (NO_USER, None, 20, None, 18),
    (NO_USER, None, None, 0, 18),
    (1, 'dfriend', 7, 0, 7),
    (1, 'dfriend', 5, 0, 5),
    (1, 'dfriend', 10, 0, 7),
    (1, 'dfriend', None, 0, 7),
    (1, 'dfriend', 5, 8, 0),
    (1, 'dfriend', 4, 3, 4),
    (1, 'dfriend', 3, 18, 0),
    (1, 'dfriend', 5, 1, 5),
    (1, 'dfriend', 0, 3, 0),
    (2, 'billybob', 7, 0, 7),
    (2, 'billybob', 15, 0, 7),
    (2, 'billybob', 2, 0, 2),
    (2, 'billybob', None, 0, 7)
)))
def test_log_query(client, log, user_id, username, nlogs, offset, expected_nlogs):
    """
    Testing the endpoint <api>/log/query
    """

    with client:
        client.get('/')
        response = log.query(username, nlogs, offset)
        assert response.status_code == statuscodes.SUCCESS
        assert len(response.json) == expected_nlogs
        
        prevdate = None
        prevtime = None
        for i, entry in response.json.items():
            if(prevdate is None) and (prevtime is None):
                prevdate = datetime.strptime(entry['verifDate'], "%Y-%m-%d")
                prevtime = datetime.strptime(entry['verifTime'], "%H:%M:%S")
            
            # Ensure all dates/times are sorted in descending order
            if prevdate == datetime.strptime(entry['verifDate'], "%Y-%m-%d"):
                assert prevtime >= datetime.strptime(entry['verifTime'], "%H:%M:%S")
            else:
                assert prevdate >= datetime.strptime(entry['verifDate'], "%Y-%m-%d")

            assert (user_id == NO_USER) or (user_id == entry['user_id'])

            prevdate = datetime.strptime(entry['verifDate'], "%Y-%m-%d")
            prevtime = datetime.strptime(entry['verifTime'], "%H:%M:%S")
