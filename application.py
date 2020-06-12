from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_session import Session
import os
from models import db, User
from forms import SignUpForm
from passlib.hash import sha256_crypt
from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
sess = Session()
SECRET_KEY = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
db.init_app(app)

def main():
    sess.init_app(app)
    db.create_all()
    

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if session.get('logged_in'):
			return f(*args, **kwargs)
		else:
			flash("You need to login first")
			return redirect(url_for('login'))
	return wrap

def logout_required(f):
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        if not session.get('logged_in'):
            return f(*args, **kwargs)
        else:
            return redirect(url_for('chat'))
    return wrapped_view


@app.route('/<path:urlpath>/')
@app.route('/', methods=['POST', 'GET'])
def index(urlpath='/'):
    if session.get('logged_in'):
        return redirect(url_for('chat'))
    else:
        form = SignUpForm()
        return render_template('main/home.html', form=form)


@app.route('/sign-up/', methods=['POST', 'GET'])
@logout_required
def sign_up():
    form = SignUpForm()
    print("validating...")
    if form.validate_on_submit():
        try:
            hashed_password = sha256_crypt.hash(form.password.data)
            firstname = form.firstname.data
            lastname = form.lastname.data
            username = form.username.data
            email = form.email.data
            password = hashed_password
            terms = form.tos.data
            l = User.query.filter_by(username=username).first()
            u = User.query.filter_by(email=email).first()
            if l is None:
                if u is None:
                    User.add_user(firstname=firstname, lastname=lastname, username=username,
                            email=email, password=password, terms=terms)
                    print("validated...")
                    flash("You have been signed up successfully! Now login your details")
                    return redirect(url_for('login'))
                else:
                    flash("Email taken already")
            else:
                flash("Username already exists.")
        except Exception as e:
            flash(e)
            return redirect(url_for('index'))
    return render_template('main/home.html', form=form)
    

@app.route('/login/', methods=['POST', 'GET'])
@logout_required
def login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            u = User.query.filter_by(username=username).first()
            try:    
                v = sha256_crypt.verify(password, u.password)
            except:
                pass
            if u and v:
                print("Validated!")
                session["logged_in"] = True
                session["username"] = u.username
                print(session["logged_in"], session["username"])
                flash(f"You are now logged in!")
                return redirect(url_for('chat'))
            else:
                flash("Invalid Login Details!")
        else:
            pass
    except Exception as e:
        print(e)

    return render_template('main/login.html')

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/chat/')
@login_required
def chat():
    return render_template('main/chat.html')


if __name__ == "__main__":
    with app.app_context():
        main()