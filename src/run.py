import logging
from views import *

from flask import Flask, render_template

if __name__ == '__main__':
    app = Flask(__name__)

    from config import csrf_key
    app.secret_key = csrf_key

    # --------- 注册蓝图 --------- #
    app.register_blueprint(login_register, url_prefix='/login_register')
    app.register_blueprint(verify, url_prefix='/verify')
    app.register_blueprint(home, url_prefix='/home')

    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.DEBUG)
    #Level: DEBUG < INFO < WARING < ERROR < CRITICAL
    #大于等于设置Level级别的日志记录会被输出

    app.run(host="192.168.1.109", port=8080)