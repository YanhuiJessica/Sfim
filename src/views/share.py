from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from models import User, Share
import secret

share = Blueprint('share', __name__)

@share.route('/ensure', methods=['POST'])
@login_required
def post_share():
    import random, string
    from passlib.hash import argon2
    from config import domain_name

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
    # 慢速哈希分享码并存储
    hashShareKey = argon2.using(rounds=256, memory_cost=1024).hash(ShareKey)
    share.add_share(user, fid, hashShareKey, nonce, enc_key)

@share.route('/verify')
def verify_share():
    from models import File
    from forms import EnsureForm

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