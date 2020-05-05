from sqlalchemy import Column, String, ForeignKey, text, TIMESTAMP
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from database import db

class Message(db.Model):

    __tablename__ = 'message'
    id_ = Column(INTEGER(11), primary_key=True)
    send_to_user = Column(INTEGER(11), nullable=False)
    send_from_user = Column(String(255), nullable=False)
    shareid = Column(INTEGER(11), nullable=False)
    filename = Column(String(255))
    read_status =  Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    send_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def create_msg(cls, send_to_usr, send_from_usr, sid, fn):
        msg = Message(send_to_user=send_to_usr, send_from_user=send_from_usr, shareid=sid, filename=fn)
        db.session.add(msg)
        db.session.commit()

    @classmethod
    def get_msg_tips(cls, uid):
        return cls.query.filter(Message.send_to_user == uid).order_by(Message.send_time.desc()).all()

    @classmethod
    def set_readed(cls, mid):
        msg = cls.get_by(id_ = mid)
        msg.read_status = 1
        db.session.commit()

    @classmethod
    def delete_msg(cls, mid):
        msg = cls.get_by(id_ = mid)
        if msg:
            db.session.delete(msg)
            db.session.commit()