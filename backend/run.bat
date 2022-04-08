@ECHO OFF
IF NOT EXIST venv\ (
    pip install virtualenv
    python -m venv venv
    CALL venv\Scripts\activate
    pip install -r requirements.txt
) ELSE (
    CALL venv\Scripts\activate
)
SET FLASK_APP=de1loc
SET FLASK_ENV=development

IF "%1" == "/i" (
    flask init-db
)

IF "%2" == "/t" (
    flask train-model
)

IF "%1" == "/s" (
    flask run --cert=cert.pem --key=key.pem
) ELSE (
    IF "%2" == "/s" (
        flask run --cert=cert.pem --key=key.pem
    ) ELSE (
        flask run
    )
)
