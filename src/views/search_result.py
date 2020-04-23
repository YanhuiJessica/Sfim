from flask import Blueprint, request, render_template, flash, redirect
from flask_login import login_required, current_user
from models.friend import Friend

search_result = Blueprint('search_result', __name__)

@search_result.route('')
@login_required
def all_users():
    user = current_user
    result = Friend.find_user('')
    return render_template('search_result.html', user=user, users=result)

@search_result.route('/', methods=['GET'])
@login_required
def manage_request():
    user = current_user
    search_info = request.args.get('search_str')
    if search_info is not None:
        result = Friend.find_user(search_info)
        return render_template('search_result.html', user=user, users=result, \
            search_str=search_info, total=len(result))
    else:
        return add_user()

def add_user():
    user = current_user
    fmail = request.args.get('umail')
    plus = request.args.get('plus')
    if user.mail == fmail:
        flash('您不能添加自己！')
    elif Friend.is_friends(user.usrid, fmail):
        flash('您与 ' + fmail + ' 已是好友，不能重复添加！')
    else:
        Friend.add_friends(user.usrid, fmail)
        flash('添加好友成功！')
    return redirect('/search_result')