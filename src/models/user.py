from database import db
from flask_login import UserMixin
from config import api_key, domain_name

# mail support - Mailgun
# templating language - Handlebars

# authcode 长度
authlen = 25

# 用户应在自注册起 24 小时内完成邮箱验证
verify_available_time_in_second = 86400
# 单个验证链接的有效时间为 10 分钟
link_available_time_in_second = 600

class User(UserMixin, db.Model):
    __tablename__ = 'users'

	@classmethod
	def get_by(cls, **kwargs):
		return cls.query.filter_by(**kwargs).first()

	@classmethod
	def del_by(cls, **kwargs):
		return cls.query.filter_by(**kwargs).delete()

	@classmethod
	def send_verify_email(cls, name, email, token, authcode):
		import requests, json

		return requests.post(
		"https://api.mailgun.net/v3/" + domain_name + "/messages",
		auth=("api", api_key),
		data={"from": "Sfim <mail@" + domain_name + ">",
			"to": "New Sfimer <" + email + ">",
			"subject": "【验证邮件】欢迎来到 Sfim ！",
			"template": "sfim_active",
            "o:tag": ['Sfim', 'Verify Email'],
            "h:X-Mailgun-Variables": json.dumps({
                "name": name,
                "verify_link": "http://" + domain_name + "/verify?token=" + token + \
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
		elif(not isVaild(0, user.create_time)):
			User.del_by(token = token)
			return 3
		elif(user.authcode != authcode or not isVaild(1, user.generate_time)):
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
