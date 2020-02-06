import os

mysql_host = os.environ.get("DB_HOST", default="localhost")
mysql_user = os.environ.get("DB_USER", default="root")
mysql_password = os.environ.get("DB_PSW", default="test4321")
mysql_schema = os.environ.get("DB_SCHEMA", default="sfim")

csrf_key = os.environ.get("CSRF_KEY", default="3a81a2312e3f449dc7b925b95f0550c2-f8faf5ef-ea8b471d")

domain_name = os.environ.get("SFIM_DOMAIN_NAME", default="sfim.tools")

api_key = os.environ.get("MAILGUN_API_KEY", default="key-1670ec1054587094aa967ece6fcb2b53")