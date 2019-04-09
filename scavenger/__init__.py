import os

from flask import Flask, request, redirect, render_template
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap(app)
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'scavenger.sqlite'),
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

    # Setup the database
    from scavenger import db
    db.init_app(app)

    # Register blueprints (organizing routes)
    from . import auth
    app.register_blueprint(auth.bp)

    from . import play
    app.register_blueprint(play.bp)

    @app.route('/hello')
    def hello():
        return 'Hello! It\'s working!'

    @app.route('/', methods=['GET', 'POST'])
    def route():
        if request.method == 'POST':
            # If JOIN
            # elif QUIT
            # elif leaders
            # elif photo
            # else return a generic help message
            print('temp')
        else:
            return render_template('index.html', data=None)

    return app