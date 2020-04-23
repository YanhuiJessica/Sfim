from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func
from database import db
from models.user import User

class Friend(db.Model):
    __tablename__ = 'friends'

    usrid = Column(INTEGER(11), primary_key=True)
    friendid = Column(INTEGER(11), primary_key=True)

    @classmethod
    def find_user(cls, search_info):
        return User.get_like(search_info)