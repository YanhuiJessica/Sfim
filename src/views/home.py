from flask import Blueprint, render_template
from flask_login import login_required, current_user

home = Blueprint('home', __name__)

@home.route('')
@login_required
def index():
    from models import File

    user = current_user
    files = File.query.filter(File.uid == user.usrid).all()
    return render_template('index.html', user=user, files=files)