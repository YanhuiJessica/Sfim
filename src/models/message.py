from sqlalchemy import Column, ForeignKey, text, TIMESTAMP
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from database import db

class Message(db.Model):

    __tablename__ = 'message'
    id_ = Column(INTEGER(11), primary_key=True)
    send_to_user = Column(INTEGER(11), nullable=False)
    send_from_user = Column(INTEGER(11), nullable=False)
    shareid = Column(INTEGER(11), nullable=False)
    read_status =  Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    send_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

    @classmethod
    def create_msg(cls, send_to_usr, send_from_usr, sid):
        msg = Message(send_to_user=send_to_usr, send_from_user=send_from_usr, shareid=sid)
        db.session.add(msg)
        db.session.commit()