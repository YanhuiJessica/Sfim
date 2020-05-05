import os

mysql_host = os.environ.get("DB_HOST", default="localhost")
mysql_user = os.environ.get("DB_USER", default="root")
mysql_password = os.environ.get("DB_PSW", default="test4321")
mysql_schema = os.environ.get("DB_SCHEMA", default="sfim")

token_expired = float(os.environ.get("TOKEN_EXPIRED", default=600))

storage_path = os.environ.get("STORAGE_PATH", default="storage/")
shared_path = os.environ.get("shared_path", default="shared/")

authlen = os.environ.get("AUTHCODE_LEN", default=25)
# 用户应在自注册起 24 小时内完成邮箱验证
verify_available_time_in_second = os.environ.get("VERIFY_AVAILABLE", default=86400)
# 单个验证链接的有效时间为 10 分钟
link_available_time_in_second = os.environ.get("LINK_AVAILABLE", default=600)

csrf_key = os.environ.get("CSRF_KEY", default="3a81a2312e3f449dc7b925b95f0550c2-f8faf5ef-ea8b471d")

domain_name = os.environ.get("SFIM_DOMAIN_NAME", default="sfim.tools")

allowed_file_list = tuple(os.environ.get("ALLOWED_SUFFIX", default="\
'image/jpeg', 'image/png','application/pdf', 'image/bmp','image/gif', \
 'application/msword', \
 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',\
 'application/vnd.ms-excel',\
 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', \
 'application/vnd.ms-powerpoint', \
 'application/vnd.openxmlformats-officedocument.presentationml.presentation'").replace("'", "").replace(" ", "").split(','))

api_key = os.environ.get("MAILGUN_API_KEY", default="key-1670ec1054587094aa967ece6fcb2b53")
sy_private_key = os.environ.get('SY_PRIVATE_KEY', default='5e49835ca1e8073180d51b7725622f04270f62950a499f18946fafceef8efb07')
sy_public_key = os.environ.get('SY_PUBLIC_KEY', default='5e49835ca1e8073180d51b7725622f04270f62950a499f18946fafceef8efb07')