from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(PasswordForm):
    email=StringField('email', validators=[DataRequired(),Email()])
    username = StringField('username', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])
    signin_sub = SubmitField('Register')

class LoginForm(PasswordForm):
    email=StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    login_sub = SubmitField('Login')