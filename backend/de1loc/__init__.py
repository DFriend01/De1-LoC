import os
import firebase_admin
from flask import Flask, json, jsonify, make_response
from . import db, user, code, auth, log

# https://flask.palletsprojects.com/en/2.0.x/tutorial/
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'de1loc.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return jsonify({"num" : 123}), 200

    # Initialize the database
    db.init_app(app)

    # Blueprints
    app.register_blueprint(user.bp)
    app.register_blueprint(code.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(log.bp)

    firebase_app = firebase_admin.initialize_app()

    return app