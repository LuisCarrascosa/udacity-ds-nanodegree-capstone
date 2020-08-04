import sqlite3
import numpy as np
# import click
from flask import current_app, g
# from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:     
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )

        g.db.row_factory = sqlite3.Row

        init_db(g.db)

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db(db):
    # db = get_db()

    sqlite3.register_adapter(np.int64, lambda val: int(val))
    sqlite3.register_adapter(np.int32, lambda val: int(val))

    # with current_app.open_resource('schema.sql') as f:
    with current_app.open_resource('schema_docker.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    app.teardown_appcontext(close_db)
    # app.cli.add_command(init_db_command)


# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')
