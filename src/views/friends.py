from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from models.friend import Friend, User

friends = Blueprint('friends', __name__)

@friends.route('')
@login_required
def list_group():
    user = current_user
    uid = user.usrid
    friendships = Friend.get_friendship(uid)
    friends = []
    for fs in friendships:
        if fs.usrid == uid:
            friends.append(User.get_by(usrid=fs.friendid))
        else:
            friends.append(User.get_by(usrid=fs.usrid))
    return render_template('friends.html', user=user, total=len(friends), friends=friends)

@friends.route('/delete', methods=['GET'])
@login_required
def break_friendship():
    user = current_user
    fmail = request.args.get('fmail')
    Friend.del_friends(user.usrid, fmail)
    flash('好友 ' + fmail + '删除成功！')
    return redirect('/friends')