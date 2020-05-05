from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import Message

msg_box = Blueprint('msg_box', __name__)

@msg_box.route('')
@login_required
def show_msg():
    user = current_user
    msg = Message.get_msg_tips(user.usrid)
    return render_template('messages.html', user=user, messages=msg)

@msg_box.route('/show_detail', methods=['POST'])
@login_required
def show_msg_detail():
    from config import domain_name, sy_private_key
    from flask import jsonify
    from models import Share
    import secret

    shareid = request.form['sid']
    msgid = request.form['mid']
    share = Share.get_by(id_ = shareid)
    Message.set_readed(msgid)
    link = 'http://' + domain_name + '/share/verify?fid=' + str(share.fid) + '&nonce=' + share.nonce
    # 使用服务器私钥解密分享码
    sk = secret.decrypt(bytes.fromhex(sy_private_key), share.enc_sharekey)
    return jsonify(link=link, sharekey=sk.hex())