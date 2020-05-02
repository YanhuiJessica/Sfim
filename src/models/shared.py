from sqlalchemy import Column, CHAR, text, String, ForeignKey, VARBINARY, TIMESTAMP
from sqlalchemy.dialects.mysql import INTEGER
from database import db
from config import storage_path, shared_path
from os import mkdir, path

class Share(db.Model):

    __tablename__ = 'share'
    id_ = Column(INTEGER(11), primary_key=True)
    fid = Column(ForeignKey('files.fileid'), nullable=False)
    share_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))
    enc_key = Column(VARBINARY(1023), nullable=False)
    sharekey = Column(CHAR(255), nullable=False)
    nonce = Column(CHAR(8), nullable=False)

    @classmethod
    def get_by(cls, **kwargs):
		return cls.query.filter_by(**kwargs).first()

    @classmethod
    def add_share(cls, user, fid, ShareKey, nonce, enc_key):
        shared_file = Share(fid=fid, sharekey=ShareKey, nonce=nonce, enc_key=enc_key)
        db.session.add(shared_file)
        db.session.commit()

    @classmethod
    def decrypt_and_encrypt(cls, fid, user, sym_key):
        from .file import File
        from .online_user import OnlineUser
        import secret

        # 获取私钥解密获得对称密钥
        usr = OnlineUser.query.filter(OnlineUser.usrid == user.usrid).first()
        Pk = usr.Pk
        enc_key = secret.decrypt(Pk, user.symkey)
        # 查询、读取本地存储的加密文件
        f = File.get_by(fileid = fid)
        hash_value = f.sha256
        with open(storage_path + str(user.usrid) + '/' + hash_value, 'rb') as f:
            content = f.read()

        # 解密文件
        content = secret.symmetric_decrypt(enc_key, content)
        # 用私钥签名
        sig = secret.sign(Pk, content)
        # 用新的会话密钥加密文件
        new_content = secret.symmetric_encrypt(sym_key, content)
        # 写入 shared_path
        user_id = str(user.usrid) + '/'
        head = shared_path + user_id
        full_path = head + hash_value
        if not path.exists(head):
            if not path.exists(shared_path):
                mkdir(shared_path)
            mkdir(head)

        # 判断文件是否存在
        # 分享文件夹要写入签名
        if not path.exists(full_path):
            with open(full_path, 'wb') as f:
                f.write(new_content)
            with open(full_path + '.sig', 'wb') as f:
                f.write(sig)