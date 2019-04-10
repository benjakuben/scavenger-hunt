import os

from flask import Flask, request, redirect, render_template, url_for
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

    from . import sender
    app.register_blueprint(sender.bp)

    @app.route('/hello')
    def hello():
        return 'Hello! It\'s working!'

    @app.route('/', methods=['GET', 'POST'])
    def route():
        if request.method == 'POST':
            """Send a dynamic reply to an incoming text message"""
            # Get the message the user sent our Twilio number
            body = request.values.get('Body', None)

            # Check for a photo
            num_media = int(request.form.get('NumMedia', 0))

            # Determine the right reply for this message
            if body.upper() == 'JOIN':
                return redirect(url_for('auth.process_join'))
            elif body.upper() == 'Q':
                return redirect(url_for('auth.process_quit'))
            elif body.upper() == 'LEADERS':
                return redirect(url_for('play.show_leaderboard'))
            elif num_media > 0:
                return redirect(url_for('play.process_photo'))
            else: 
                # return a generic help message
                print('temp')
        else:
            return render_template('index.html', data=None)

    return app