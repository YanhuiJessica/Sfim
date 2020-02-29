import os

mysql_host = os.environ.get("DB_HOST", default="localhost")
mysql_user = os.environ.get("DB_USER", default="root")
mysql_password = os.environ.get("DB_PSW", default="test4321")
mysql_schema = os.environ.get("DB_SCHEMA", default="sfim")

token_expired = float(os.environ.get("TOKEN_EXPIRED", default=600))

authlen = os.environ.get("AUTHCODE_LEN", default=25)
# 用户应在自注册起 24 小时内完成邮箱验证
verify_available_time_in_second = os.environ.get("VERIFY_AVAILABLE", default=86400)
# 单个验证链接的有效时间为 10 分钟
link_available_time_in_second = os.environ.get("LINK_AVAILABLE", default=600)

csrf_key = os.environ.get("CSRF_KEY", default="3a81a2312e3f449dc7b925b95f0550c2-f8faf5ef-ea8b471d")

domain_name = os.environ.get("SFIM_DOMAIN_NAME", default="sfim.tools")

api_key = os.environ.get("MAILGUN_API_KEY", default="key-1670ec1054587094aa967ece6fcb2b53")