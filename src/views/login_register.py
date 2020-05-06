from flask import Blueprint, render_template, redirect, url_for, make_response
from forms import RegisterForm, LoginForm
import re, logging, secret
from flask import current_app as app
from flask_login import login_user, current_user

login_register = Blueprint('login_register',__name__)
username_pattern = re.compile(r'[\u4e00-\u9fa5a-zA-Z0-9_]+')

@login_register.route('/')
def get_login_register():
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))

    return render_template('login_register.html',login_form=LoginForm(),register_form=RegisterForm())

@login_register.route('/', methods=['POST'])
def post_login_register():
    from models import User, OnlineUser

    login_form = LoginForm()
    signin_form = RegisterForm()

    # http://www.pythondoc.com/flask-login/#flask-login
    if(login_form.login_sub.data):
        try:
            import flask, traceback
            from hashlib import sha256
            from passlib.hash import argon2

            assert login_form.validate_on_submit(), '无效填写'
            email = login_form.email.data
            user = User.get_by(mail=email)
            assert user, "该用户不存在"
            saved = user.hashword
            password = login_form.password.data
            check_status = argon2.verify(password, saved)
            assert check_status, "邮箱或密码输入错误"
            assert user.verification_status == 1 or User.isValid(0, user.create_time), \
                User.del_by(token=user.token) and "注册失败！您需要重新注册"
            assert user.verification_status == 1, "尚未激活账户，请前往邮箱激活"
            digest = sha256(password.encode('utf-8')).hexdigest()
            decrypted_prikey = secret.symmetric_decrypt(bytes.fromhex(digest), user.privkey)
            token = OnlineUser.create_record(user.usrid, decrypted_prikey)
            login_user(user)
            next = flask.request.args.get('next')
            # next_is_valid should check if the user is valid
            # permission to access the `next` url
            resp = make_response(redirect(next or url_for('home.index')))
            resp.set_cookie('token', token)
            return resp
        except AssertionError as e:
            message = e.args[0] if len(e.args) else str(e)
            return render_template('login_register.html', login_form = login_form, register_form = signin_form, \
                message = message)

    if(signin_form.signin_sub.data):
        try:
            assert signin_form.validate_on_submit(), '无效填写'
            email = signin_form.email.data
            user = signin_form.username.data
            assert username_pattern.fullmatch(user), '用户名只能包含汉字、英文、数字及下划线'
            assert len(user) <= 15, '用户名长度不得超过15个字符'
            password = signin_form.password.data
            confirm_passwd = signin_form.confirm_password.data
            assert len(password) >= 6, '密码长度至少为6位'
            assert password == confirm_passwd, '两次密码不相等'
            hash_password = signin_form.get_password_hash()
            User.create_user(email, user, password, hash_password)
            return render_template('login_register.html', login_form = login_form, register_form = signin_form, \
                message = "注册成功！离使用 Sfim 只差一步！请前往邮箱激活您的账户。")
        except AssertionError as e:
            if(traceback):
                logging.warning(traceback.format_exc())
            message = e.args[0] if len(e.args) else str(e)
            return render_template('login_register.html', login_form = login_form, register_form = signin_form, \
                message = message)
