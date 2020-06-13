# udacity-ds-nanodegree-capstone

source ~/Documentos/enviroments/desarrollo/bin/activate

$ export FLASK_APP=stock_predictor_webapp.py
$ flask run o puede ser python -m flask run
 * Running on http://127.0.0.1:5000/

Externally Visible Server
If you run the server you will notice that the server is only accessible from your own computer, not from any other in the network. This is the default because in debugging mode a user of the application can execute arbitrary Python code on your computer.

If you have the debugger disabled or trust the users on your network, you can make the server publicly available simply by adding --host=0.0.0.0 to the command line:

$ flask run --host=0.0.0.0

https://flask.palletsprojects.com/en/1.1.x/quickstart/

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')

flask init-db

import logging

from flask import Flask
from werkzeug.utils import find_modules, import_string


def configure_logging():
    # register root logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.INFO)


def register_blueprints(app):
    """Automagically register all blueprint packages
    Just take a look in the blueprints directory.
    """
    for name in find_modules('blueprints', recursive=True):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def create_app():
    app = Flask(__name__)
    configure_logging()
    register_blueprints(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()