import os
import logging

from flask import Flask


def configure_logging():
    # register root logging
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.INFO)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    configure_logging()

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    from . import auth, db, main, training, data_aquisition
    app.register_blueprint(auth.bp)
    db.init_app(app)

    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='main')

    app.register_blueprint(data_aquisition.bp)
    app.add_url_rule('/data_aquisition', endpoint='data_aquisition')

    app.register_blueprint(training.bp)
    app.add_url_rule('/training', endpoint='training')

    return app
