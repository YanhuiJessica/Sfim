from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email
from flask import current_app as app

class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()])

    def get_password_hash(self):
        from passlib.hash import argon2
        hashword = argon2.using(rounds = 256, memory_cost = 1024).hash(self.password.data)
        app.logger.debug("hashword = %s",hashword)
        return hashword

class RegisterForm(PasswordForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    username = StringField('username', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])
    signin_sub = SubmitField('Register', validators=[DataRequired()])

class LoginForm(PasswordForm):
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired()])
    login_sub = SubmitField('Login', validators=[DataRequired])
