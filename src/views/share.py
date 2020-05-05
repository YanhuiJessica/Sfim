from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models import User, Share, Message, File
from forms import EnsureForm
from passlib.hash import argon2
import secret

share = Blueprint('share', __name__)

@share.route('/ensure', methods=['POST'])
@login_required
def post_share():
    import random, string
    from config import domain_name, sy_public_key

    user = current_user
    fid = request.form['fid']
    choice = request.form['choice']
    nonce = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
    ShareKey = secret.new_symmetric_key()
    sym_key = secret.new_symmetric_key()
    # 先对称解密再用新的分享密钥对称加密
    Share.decrypt_and_encrypt(fid, user, sym_key)
    # 分享码对对称密钥加密
    enc_key = secret.symmetric_encrypt(ShareKey, sym_key)
    # 慢速哈希分享码
    hashShareKey = argon2.using(rounds=256, memory_cost=1024).hash(ShareKey)
    # 使用服务器公钥加密分享码
    enc_ShareKey = secret.encrypt(bytes.fromhex(sy_public_key), ShareKey)
    sid = Share.add_share(fid, hashShareKey, enc_ShareKey, nonce, enc_key)
    # 向指定用户发送分享消息
    choice = choice.split(',')
    for u in choice:
        Message.create_msg(User.get_by(mail=u).usrid, user.usrname, sid, File.get_by(fileid=fid).filename)
    return '分享成功！'

@share.route('/verify')
def verify_share():
    fid = request.args.get('fid')
    nonce = request.args.get('nonce')
    # 查询分享数据库中是否有该文件
    f = Share.get_by(fid = fid, nonce = nonce)
    if(not f):
        return 404
    else:
        f = File.get_by(fileid = fid)
        fname = f.filename
        uid = f.uid
        name = User.get_by(usrid = uid).usrname
        return render_template('unlock.html', form=EnsureForm(fid=fid, nonce=nonce), \
            fname=fname, name=name)

@share.route('/download', methods=['POST'])
@login_required
def download_shared():
    from config import shared_path
    from flask import make_response
    from collections import OrderedDict
    import unicodedata
    from werkzeug.urls import url_quote

    form = EnsureForm()
    fid = form.fid.data
    nonce = form.nonce.data
    sharekey = form.sharekey.data
    f = Share.get_by(fid=fid, nonce=nonce)
    if f is None:
        return 404
    else:
        # 验证分享码是否正确
        sharekey = bytes.fromhex(sharekey)
        saved = f.sharekey
        success = argon2.verify(sharekey, saved)
        if not success:
            flash('分享码不正确！')
            return redirect('/msg_box')
        # 用分享码解密获得对称密钥
        enc_key = f.enc_key
        sym_key = secret.symmetric_decrypt(sharekey, enc_key)
        f = File.get_by(fileid=fid)
        uid = f.uid
        hash_value = f.sha256
        PublicKey = User.get_by(usrid=uid).pubkey
        # 对称解密
        path = shared_path + str(uid) + '/' + hash_value
        with open(path, 'rb') as f_:
            content = f_.read()
            decrypted_content = secret.symmetric_decrypt(sym_key, content)
        response = make_response(decrypted_content)
        filename = f.filename
        filenames = OrderedDict()
        try:
            filename = filename.encode('latin-1')
        except UnicodeEncodeError:
            filenames['filename'] = unicodedata.normalize('NFKD', filename).encode('latin-1', 'ignore')
            filenames['filename*']:"UTF-8''{}".format(url_quote(filename))
        else:
            filenames['filename'] = filename
        response.headers.set('Content-Disposition', 'attachment', **filenames)
        return response