from sqlalchemy import Column, String, ForeignKey, VARBINARY, TIMESTAMP, text
from database import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class OnlineUser(db.Model):
    __tablename__ = 'online_users'

    usrid = Column(ForeignKey('users.usrid'), primary_key = True)
    token = Column(String(50), primary_key = True)
    last_used = Column(TIMESTAMP, nullable = False, server_default = \
        text("current_timestamp() ON UPDATE current_timestamp()"))
    Pk = Column(VARBINARY(255), nullable = False, server_default = text("''"))

    user = relationship('User')

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def new_available_token(cls):
        from uuid import uuid4
        record_list = cls.query.all()
        token_list = list(record.token for record in record_list)
        while True:
            token = uuid4().hex
            if token not in token_list:
                record = cls.query.filter(cls.token == token).first()
                if record is None:
                    return token

    @classmethod
    def create_record(cls, id, prikey):
        from datetime import datetime
        token = cls.new_available_token()
        record = cls.get_by(usrid = id)
        if record is None:
            record = OnlineUser(usrid = id, token = token, Pk = prikey)
            record.last_used = datetime.now()
            db.session.add(record)
        else:
            record.token = token
            record.last_used = datetime.now()
        db.session.commit()
        return token

    @classmethod
    def delete_record(cls, id):
        record = cls.get_by(usrid = id)
        if record:
            db.session.delete(record)
            db.session.commit()

    @classmethod
    def verify_token(cls, token):
        from datetime import datetime
        from config import token_expired
        record = cls.get_by(token = token)
        if record is not None:
            last_used = record.last_used
            now = datetime.now()
            delta = now - last_used
            total_seconds = delta.total_seconds()
            if total_seconds < token_expired:
                return record
        return record.usrid