from flask import Blueprint, render_template, redirect, request, url_for
from models.user import User

verify = Blueprint('verify', __name__)

@verify.route('/', methods=['GET'])
def get_verify():
    # 获取 GET 请求的参数 token 与 authcode 的值
    token = request.args.get('token')
    authcode = request.args.get('authcode')

    # 调用verify_email函数进行认证
    if token is not None and authcode is not None:
        status_code = User.verify_email(token, authcode)
        if status_code == 1:
            return redirect(url_for('verify.notfound'))
        elif status_code == 2:
            return redirect(url_for('verify.notmodify'))
        elif status_code == 3:
            return redirect(url_for('verify.fail'))
        elif status_code == 4:
            if User.link_refresh(token):
                return redirect(url_for('verify.retry'))
            else:
                return redirect(url_for('verify.efail'))
        else:
            return redirect(url_for('verify.success'))
    else:
        return redirect(url_for('verify.notfound'))

@verify.route('/success')
def success():
    return render_template('verify.html',title='激活成功！',msg='恭喜！现在您可以正常使用Sfim了！')

@verify.route('/notmodify')
def notmodify():
    return render_template('verify.html',title='Sfim',msg='您已成功激活，无需再次激活。')

@verify.route('/retry')
def retry():
    return render_template('verify.html',title='激活失败！',msg='链接已失效。已将新链接发送至您的邮箱，请注意查收邮件。')

@verify.route('/efail')
def fail():
    return render_template('verify.html',title='Ooops！',msg='包含有新链接的邮件发送失败，您可以回到登录界面点击「未收到激活邮件」，再次发送。')

@verify.route('/fail')
def fail():
    return render_template('verify.html',title='激活失败！',msg='激活时限已过！您需要重新注册。')

@verify.route('notfound')
def notfound():
    return render_template('verify.html',title='404 Not Found',msg='您所请求的页面不存在。')