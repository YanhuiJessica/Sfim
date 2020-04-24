from sqlalchemy import Column, or_
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func
from database import db
from models.user import User

class Friend(db.Model):
    __tablename__ = 'friends'

    usrid = Column(INTEGER(11), primary_key=True)
    friendid = Column(INTEGER(11), primary_key=True)

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def del_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).delete()

    @classmethod
    def find_user(cls, search_info):
        return User.get_like(search_info)

    @classmethod
    def get_friendship(cls, usrid):
        return cls.query.filter(or_(Friend.usrid == usrid, Friend.friendid == usrid)).all()

    @classmethod
    def add_friends(cls, usrid, fmail):
        friendid = User.get_by(mail = fmail).usrid
        if usrid > friendid:
            usrid, friendid = friendid, usrid
        friendship = Friend(usrid = usrid, friendid = friendid)
        db.session.add(friendship)
        db.session.commit()

    @classmethod
    def del_friends(cls, usrid, fmail):
        friendid = User.get_by(mail = fmail).usrid
        if usrid < friendid:
            cls.del_by(usrid = usrid, friendid = friendid)
        else:
            cls.del_by(usrid = friendid, friendid = usrid)

    @classmethod
    def is_friends(cls, usrid, fmail):
        friendid = User.get_by(mail = fmail).usrid
        if usrid > friendid:
            usrid, friendid = friendid, usrid
        flag = cls.get_by(usrid = usrid, friendid = friendid)
        if flag is None:
            return False
        else:
            return True