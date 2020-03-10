from flask import Blueprint, request, redirect, make_response
from flask_login import login_required, logout_user, current_user

logout = Blueprint('logout', __name__)

@logout.route('')
@login_required
def get_logout():
    from models import OnlineUser
    token = request.cookies.get('token')
    record = OnlineUser.verify_token(token)
    if current_user is not None:
        OnlineUser.delete_record(record.usrid)
        resp = make_response(redirect('/login_register'))
        resp.delete_cookie('token')
        logout_user()
        return resp
    return redirect('/login_register')