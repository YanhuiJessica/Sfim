from flask import Blueprint, render_template
from flask_login import login_required, current_user

friends = Blueprint('friends', __name__)

@friends.route('')
@login_required
def list_group():
    user = current_user
    return render_template('friends.html', user=user)