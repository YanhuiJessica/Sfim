from flask import Blueprint, render_template, redirect
from forms import RegisterForm,LoginForm

login_register = Blueprint('login_register',__name__)

@login_register.route('/')
def get_login_register():
    return render_template('login_register.html',login_form=LoginForm(),register_form=RegisterForm())
