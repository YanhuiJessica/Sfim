from flask import Blueprint, render_template, redirect
from forms import RegisterForm,LoginForm
import re

login_register = Blueprint('login_register',__name__)
username_pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9]+')

@login_register.route('/')
def get_login_register():
    return render_template('login_register.html',login_form=LoginForm(),register_form=RegisterForm())

@login_register.route('/', methods=['POST'])
def post_login_register():
    login_form = LoginForm()
    signin_form = RegisterForm()

    if(login_form.login_sub.data):
        try:
            assert login_form.validate_on_submit(), '无效填写'
        except AssertionError as e:
            message = e.args[0] if len(e.args) else str(e)

    if(signin_form.signin_sub.data):
        try:
            assert signin_form.validate_on_submit(), '无效填写'
            email = signin_form.email.data
            user = signin_form.username.data
            assert username_pattern.fullmatch(user), '用户名只能包含汉字、英文及数字'
            password = signin_form.password.data
            confirm_passwd = signin_form.confirm_password.data
        except AssertionError as e:
            message = e.args[0] if len(e.args) else str(e)

    return render_template('login_register.html',login_form=LoginForm(),register_form=RegisterForm(), message=message)