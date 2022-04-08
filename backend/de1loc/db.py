import sqlite3
import click
import os
import shutil
import re
from flask import current_app, g
from flask.cli import with_appcontext
from .FacialClassifier.model_train import trainModel

# https://flask.palletsprojects.com/en/2.0.x/tutorial/

DEFAULT_CATEGORIES = ['0', '1']
MODELDIR = 'model'
MODEL_FILENAME = 'model'

def get_db():
    """
    Gets an instance of the database.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Closes the database.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initializes the database with default entries.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('init_data.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('train-model')
@with_appcontext
def train_model_command():
    trainModel()
    click.echo('Trained the model')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(train_model_command)
