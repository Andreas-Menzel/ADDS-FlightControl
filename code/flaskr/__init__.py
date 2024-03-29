import os

from flask import Flask, url_for, redirect, jsonify
from flask_cors import CORS


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
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

    from . import db
    db.init_app(app)

    @app.route('/how_are_you')
    def how_are_you():
        return jsonify({'version': '1.0.0-alpha'})

    # register blueprints
    from . import tell
    app.register_blueprint(tell.bp)

    from . import ask
    app.register_blueprint(ask.bp)

    from . import infrastructure
    app.register_blueprint(infrastructure.bp)

    from . import ui
    app.register_blueprint(ui.bp)

    @app.route('/')
    def index():
        return redirect('/ui')

    return app
