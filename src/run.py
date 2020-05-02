import logging
from views import *

from flask import render_template
from flask_dropzone import Dropzone

if __name__ == '__main__':
    from database import create_app
    app = create_app(__name__)
    dropzone = Dropzone(app)

    from config import csrf_key
    app.secret_key = csrf_key

    # --------- 注册蓝图 --------- #
    app.register_blueprint(home, url_prefix='/home')
    app.register_blueprint(friends, url_prefix='/friends')
    app.register_blueprint(share, url_prefix='/share')
    app.register_blueprint(search_result, url_prefix='/search_result')
    app.register_blueprint(login_register, url_prefix='/login_register')
    app.register_blueprint(verify, url_prefix='/verify')
    app.register_blueprint(logout, url_prefix='/logout')

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)
    #Level: DEBUG < INFO < WARING < ERROR < CRITICAL
    #大于等于设置Level级别的日志记录会被输出

    from flask_login import LoginManager
    login_manager = LoginManager(app)

    from models import User
    @login_manager.user_loader
    def load_user(userid):
        return User.query.filter(User.usrid == int(userid)).first()

    login_manager.login_view = 'login_register.get_login_register'
    app.run(host="192.168.1.115", port=8080)