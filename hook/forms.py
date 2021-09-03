from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length


class SignUpForm(FlaskForm):
    firstname = StringField('Firstname:', validators=[DataRequired(),
                                                      Length(min=2, max=20)])
    lastname = StringField('Lastname:', validators=[DataRequired(),
                                                    Length(min=2, max=20)])
    username = StringField('Username:', validators=[DataRequired(),
                                                    Length(min=2, max=10)])
    email = StringField('Email:', validators=[DataRequired(),
                                              Length(min=2, max=30)])
    password = PasswordField('Password:', validators=[DataRequired(),
                                                      Length(min=5, max=60),
                                                      EqualTo('confirm',
                                                      message="Passwords \
                                                      must match.")]
                             )
    confirm = PasswordField('Repeat Password:')
    tos = BooleanField('I accept the terms and conditions that apply to this \
                        application.', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(),
                                                    Length(min=2, max=10)])
    password = PasswordField('Password:', validators=[DataRequired(),
                                                      Length(min=5, max=50)])
