from sqlalchemy import Column, String, VARBINARY
from sqlalchemy import CHAR, DateTime, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.sql import func
from database import db
from flask_login import LoginManager, UserMixin
from config import api_key, domain_name, authlen
from config import verify_available_time_in_second, link_available_time_in_second

# mail support - Mailgun
# templating language - Handlebars

class User(UserMixin, db.Model):
	__tablename__ = 'users'

	usrid = Column(INTEGER(11), primary_key=True)
	usrname = Column(String(255), nullable=False)
	hashword = Column(String(255), nullable=False)
	mail = Column(String(255), nullable=False)
	token = Column(String(50), nullable=False)
	authcode = Column(String(50), nullable=False)
	verification_status = Column(TINYINT(1),nullable=False,server_default=text("'0'"))
	create_time = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp()"))
	generate_time = Column(TIMESTAMP, server_default=text("current_timestamp()"))
	pubkey = Column(VARBINARY(255), nullable=False, server_default=text("''"))
	privkey = Column(VARBINARY(1023), nullable=False, server_default=text("''"))
	symkey = Column(VARBINARY(255), nullable=False, server_default=text("''"))

	def get_id(self):
		try:
			from flask_login._compat import text_type
			return text_type(self.usrid)
		except AttributeError:
			raise NotImplementedError('No `id` attribute - override `get_id`')

	@classmethod
	def get_by(cls, **kwargs):
		return cls.query.filter_by(**kwargs).first()

	@classmethod
	def get_like(cls, string):
		return list(set(cls.query.filter(User.mail.like('%' + string + '%')).all() + \
			cls.query.filter(User.usrname.like('%' + string + '%')).all()))

	@classmethod
	def del_by(cls, **kwargs):
		return cls.query.filter_by(**kwargs).delete()

	@classmethod
	def send_verify_email(cls, name, email, token, authcode):
		import requests, json

		return requests.post(
		"https://api.mailgun.net/v3/mg." + domain_name + "/messages",
		auth=("api", api_key),
		data={"from": "Sfim <mail@" + domain_name + ">",
			"to": "New Sfimer <" + email + ">",
			"subject": "【验证邮件】欢迎来到 Sfim ！",
			"template": "sfim_active",
			"o:tag": ['Sfim', 'Verify Email'],
			"h:X-Mailgun-Variables": json.dumps({
				"name": name,
					"verify_link": "http://www." + domain_name + "/verify?token=" + token + \
					"&authcode=" + authcode
				})})

	@classmethod
	def generate_verify_authcode(cls):
		import string, random

		char_set = list(string.digits + string.ascii_letters)
		random.shuffle(char_set)
		authcode = "".join(char_set[:authlen])
		return authcode

	@classmethod
	def link_refresh(cls, token):
		user = User.get_by(token = token)
		authcode = cls.generate_verify_authcode()
		return cls.send_verify_email(user.name, user.email, token, authcode).status_code == 200

	@classmethod
	def isVaild(cls, template_time_id, compare_time):
		# 判断是否在有效激活时间内或链接是否有效
		import datetime
		d = (datetime.datetime.now() - compare_time).total_seconds()
		template_time = (lambda x: verify_available_time_in_second if x == 0 \
			else link_available_time_in_second)(template_time_id)
		if(d <= template_time):
			return True
		else:
			return False

	@classmethod
	def verify_email(cls, token, authcode):
		user = User.get_by(token = token)
		if(user is None):
			return 1
		elif(user.verification_status == 1):
			return 2
		elif(not cls.isVaild(0, user.create_time)):
			User.del_by(token = token)
			return 3
		elif(user.authcode != authcode or not cls.isVaild(1, user.generate_time)):
			return 4
		else:
			user.verification_status = 1
			return 0

	@classmethod
	def create_user(cls, mail, name, password, hashword):
		import secret
		from hashlib import sha256, md5

		user = User.get_by(mail = mail)
		assert user is None, '填写的注册邮箱已存在'
		token = md5(("%s%s"%(name,mail)).encode('utf-8')).hexdigest()
		authcode = User.generate_verify_authcode()
		assert User.send_verify_email(name, mail, token, authcode).status_code == 200, \
			"验证邮件发送失败"

		# 随机生成一个用户的对称密钥与公私钥
		symmetric_key = secret.new_symmetric_key()
		private_key, public_key = secret.new_pair()
		# 用用户的密码对用户的私钥加密（对称加密）
		digest = sha256(password.encode('utf-8')).hexdigest()
		encrypted_prikey = secret.symmetric_encrypt(bytes.fromhex(digest), private_key)
		# 对对称密钥加密
		encrypted_symkey = secret.encrypt(private_key, symmetric_key)
		user = User(usrname = name, hashword = hashword,
					mail = mail, token = token, authcode = authcode,
					symkey = encrypted_symkey, privkey = encrypted_prikey,
					pubkey = public_key)
		db.session.add(user)
		db.session.commit()
