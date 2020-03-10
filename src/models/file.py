from sqlalchemy import Column, String, CHAR, TIMESTAMP, text, and_
from sqlalchemy.dialects.mysql import INTEGER
from os import path, mkdir, remove
from config import storage_path
from models.online_user import OnlineUser
from models.user import User
from database import db
import re, secret

filename_pattern = re.compile(r'[^\\/:*?"<>|]+')

def convert_bytes(num):
    # convert bytes to MB.... GB... etc
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

class File(db.Model):
    __tablename__ = 'files'

    fileid = Column(INTEGER(11), primary_key=True)
    filename = Column(String(255))
    size = Column(String(255), nullable=False)
    sha256 = Column(CHAR(255), nullable=False)
    uid = Column(INTEGER(11), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))

    @classmethod
    def upload_file(cls, user, data):
        from hashlib import sha256
        from config import allowed_file_list

        filename = data.filename
        assert len(filename) <= 64, '文件名过长（>64B）'
        assert filename_pattern.fullmatch(filename), '文件名中不能包含以下字符：\n\\ / : * ? " < > |'
        import magic
        mime_type = str(magic.from_buffer(data.read(), mime=True))
        assert mime_type in allowed_file_list, '不支持的文件类型'

        content = data.read()
        hash_value = sha256(content).hexdigest()
        f = File.query.filter(and_(File.uid == user.usrid, File.sha256 == hash_value)).first()
        assert not f, '文件已存在'
        size = convert_bytes(len(content))
        assert len(content) < 20*1024*1024, '文件过大（>=20MB）'
        userid = str(user.usrid) + '/'
        hash_value = sha256(content).hexdigest()
        head = storage_path + userid
        if not path.exists(head):
            if not path.exists(storage_path):
                mkdir(storage_path)
            mkdir(head)
        if not path.exists(head + hash_value):
            # 还原对称密钥
            Pkv = OnlineUser.get_by(usrid = userid).Pk
            encrypted_symkey = User.get_by(usrid = userid).symkey
            symkey = secret.decrypt(Pkv, encrypted_symkey)
            # 加密
            content = secret.symmetric_encrypt(symkey, content)
            # 只保存密文
            with open(head + hash_value, 'wb') as f:
                f.write(content)
        fi = File(uid=user.usrid, filename=filename, size=size, sha256=hash_value)
        db.session.add(fi)
        db.session.commit()

    @classmethod
    def delete_file(cls, user, fid):
        f = File.query.filter(File.fileid == fid).first()
        assert f, '文件不存在'
        sha256 = f.sha256
        db.session.delete(f)
        db.session.commit()
        remove(storage_path + str(user.usrid) + '/' + sha256)

    @classmethod
    def download_file(cls, user, fid, type_):
        from flask import make_response, send_file
        from collections import OrderedDict
        import unicodedata
        from werkzeug.http import dump_options_header
        from werkzeug.urls import url_quote

        f = File.query.filter(File.fileid == fid).first()
        assert f, '文件不存在'
        hash_value = f.sha256
        filename = f.filename
        user_ = OnlineUser.query.filter(OnlineUser.usrid == user.usrid).first()
        # 获取私钥解密得对称密钥
        Pk = user_.Pk
        enc_key = secret.decrypt(Pk, user.symkey)
        with open(storage_path + str(user.usrid) + '/' + hash_value, 'rb') as f_:
            content = f_.read()
            if type_ == 'encrypted':
                filename = filename + '.encrypted'
            elif type_ == 'hashvalue':
                content = hash_value
                filename = filename + '.hash'
            else:
                content = secret.symmetric_decrypt(enc_key, content)
                if type_ == 'signature':
                    content = secret.sign(Pk, content)
                    filename = filename + '.sig'
            response = make_response(content)
            filenames = OrderedDict()
            try:
                filename = filename.encode('latin-1')
            except UnicodeEncodeError:
                filenames['filename'] = unicodedata.normalize('NFKD', filename).encode('latin-1', 'ignore')
                filenames['filename*']: "UTF-8''{}".format(url_quote(filename))
            else:
                filenames['filename'] = filename
            response.headers.set('Content-Disposition', 'attachment', **filenames)
            return response