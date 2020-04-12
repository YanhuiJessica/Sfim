from flask import Blueprint, render_template, flash, redirect, request
from flask_login import login_required, current_user
from models import File

home = Blueprint('home', __name__)

@home.route('')
@login_required
def index():
    user = current_user
    files = File.query.filter(File.uid == user.usrid).all()
    return render_template('index.html', user=user, files=files)

@home.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('home_upload.html')
    else:
        try:
            user = current_user
            f = request.files.get('file')
            File.upload_file(user, f)
            flash('上传成功！')
        except AssertionError as e:
            message = e.args[0] if len(e.args) else str(e)
            return message, 400
        return redirect('/home')

@home.route('/remove')
@login_required
def get_remove():
    try:
        user = current_user
        fid = request.args.get('fid')
        File.delete_file(user, fid)
        flash('删除成功！')
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('删除失败！' + message)
    return redirect('/home')

@home.route('/download')
@login_required
def get_download():
    try:
        user = current_user
        fid = request.args.get('fid')
        assert fid, 'missing fid'
        ty = request.args.get('type')
        assert ty, 'missing type'
        assert ty in ('encrypted', 'plaintext', 'signature', 'hashvalue', 'publickey'), 'unknown type'
        return File.download_file(user, fid, ty)
    except AssertionError as e:
        message = e.args[0] if len(e.args) else str(e)
        flash('下载失败！' + message)
        return redirect('/home')