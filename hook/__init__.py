import os

from flask import Flask, redirect, render_template, session, url_for
from flask_session import Session
from flask_socketio import SocketIO

from hook.forms import LoginForm, SignUpForm
from hook.models import db

socketio = SocketIO()


# returns flask application objects
def create_app(test_config=None, debug=False):
    """ application's factory """
    app = Flask(__name__)

    # secret key autogenerated
    SECRET_KEY = os.urandom(32)

    app.config.from_mapping(
        SESSION_PERMANENT=False,
        SESSION_TYPE="filesystem",
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL') or \
            'sqlite:///' + os.path.join(os.path.abspath('.'), 'data-dev.sqlite'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY=SECRET_KEY,
        debug=debug
    )

    if test_config is None:
        # load the app config from file if not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # if testing load app config on tests config
        app.config.from_mapping(test_config)

    @app.route('/<path:urlpath>/')
    @app.route('/', methods=['POST', 'GET'])
    def index(urlpath='/'):
        """ homepage for all non-registered users """
        # if user not in session, form pop's up
        if session.get('user'):
            return redirect(url_for('chat.index'))
        signup_form = SignUpForm()
        login_form = LoginForm()
        return render_template('main/home.html', signup_form=signup_form,
            login_form=login_form)

    @app.errorhandler(505)
    def internal_server_error():
        flash("Error")
        return redirect(url_for('index'))

    from hook.routes.auth import auth
    app.register_blueprint(auth, url_prefix='/auth/')

    from hook.routes.chat import chat
    app.register_blueprint(chat, url_prefix='/chat/')

    # initializes app and configures sessions
    db.init_app(app)
    Session(app)
    socketio.init_app(app)

    return app
