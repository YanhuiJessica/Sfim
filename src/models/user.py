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
	def generate_verify_token(cls, name, mail):
		import string, random
		from hashlib import md5

		token = md5(("%s%s"%(name,mail)).encode('utf-8')).hexdigest()
		char_set = list(string.digits + string.ascii_letters)
        random.shuffle(char_set)
		authcode = "".join(char_set[:authlen])
		return token, authcode

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
	def create_user(cls, mail, name, password, hashword):
		import secret
        from hashlib import sha256

		user = User.get_by(mail = mail)
		assert user is None, '填写的注册邮箱已存在'
		token, authcode = User.generate_verify_token(name, mail)
		assert User.send_verify_email(name, mail, token, authcode).status_code == 200, \
			"验证邮件发送失败"
