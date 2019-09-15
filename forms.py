from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField,HiddenField
from wtforms.validators import DataRequired, Length, Email

class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])

class RegisterForm(PasswordForm):
    email=StringField('email', validators=[DataRequired(),Email()])
    username = StringField('username', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])

class LoginForm(PasswordForm):
    email=StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])