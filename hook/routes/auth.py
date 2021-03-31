from flask import (Blueprint, session, flash,
                   redirect, url_for, render_template, request
                   )
from functools import wraps
from hook.models import User
from hook.forms import SignUpForm
from passlib.hash import sha256_crypt


auth = Blueprint('auth', __name__)


def login_required(f):
    """ user login check wrapper """
    @wraps(f)
    def wrap(*args, **kwargs):
        """ checks if user in session """
        if session.get('user'):
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('auth.login'))
    return wrap


def logout_required(f):
    """ user logout check wrapper """
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        """ checks if user not in session """
        if not session.get('user'):
            return f(*args, **kwargs)
        else:
            # if user in session redirects to chat
            flash('You need to logout first.')
            return redirect(url_for('chat.index'))
    return wrapped_view


@auth.route('sign-up/', methods=['POST', 'GET'])
@logout_required
def sign_up():
    """ registers user on post request """
    form = SignUpForm()
    # validate users information and form submissioin
    if form.validate_on_submit():
        print("Submitting...")
        try:
            hashed_password = sha256_crypt.hash(form.password.data)
            firstname = form.firstname.data
            lastname = form.lastname.data
            username = form.username.data
            email = form.email.data
            password = hashed_password
            terms = form.tos.data
            existing_user = User.query.filter_by(username=username).first()
            u = User.query.filter_by(email=email).first()
            # checks if username exists before, if true error
            if existing_user is None:
                if u is None:
                    # adds user to db
                    new_user = User(firstname=firstname, lastname=lastname,
                                    username=username, email=email,
                                    password=password, terms=terms)
                    new_user.save()

                    flash("You have been signed up successfully!")
                    return redirect(url_for('auth.login'))
                else:
                    # email taken error flash
                    flash("Email taken already")
            else:
                # username exists error flash
                flash("Username already exists.")
        except Exception as e:
            print(e)
            raise e
            return redirect(url_for('index'))
    return render_template('main/home.html', form=form)


@auth.route('login/', methods=['POST', 'GET'])
@logout_required
def login():
    """ verify if user exists in the database """
    if request.method == "POST":
        try:
            # checks if user exists
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()
            secret = sha256_crypt.verify(password, user.password)

            if user and secret:  # username and password
                # logs user in
                session.clear()
                session["user"] = user
                flash("You are now logged in!")
                return redirect(url_for('chat.index'))
            else:
                flash("Invalid Login Details!")
                return redirect(url_for('auth.login'))
        except Exception:
            flash('Check your credentials and try again!')
    return render_template('main/login.html')


@auth.route("logout/")
@login_required
def logout():
    """ logs out user """
    session.clear()
    flash("You logged out successfully!")
    return redirect(url_for('index'))
