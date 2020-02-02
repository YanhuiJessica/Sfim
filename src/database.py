from flask_sqlalchemy import SQLAlchemy
from config import mysql_user, mysql_password, mysql_host, mysql_schema

db = SQLAlchemy()
Base = db.Model


def create_app(name):
    from flask import Flask
    app = Flask(name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(mysql_user, mysql_password, mysql_host,mysql_schema)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app
