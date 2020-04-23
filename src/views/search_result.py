from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from models.friend import Friend

search_result = Blueprint('search_result', __name__)

@search_result.route('', methods=['GET'])
@login_required
def search_user():
    user = current_user
    search_info = request.args.get('search_str')
    result = Friend.find_user(search_info)
    return render_template('search_result.html', user=user, users=result, \
        search_str=search_info, total=len(result))