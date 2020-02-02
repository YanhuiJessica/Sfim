import os

mysql_host = os.environ.get("DB_HOST", default="localhost")
mysql_user = os.environ.get("DB_USER", default="root")
mysql_password = os.environ.get("DB_PSW", default="test4321")
mysql_schema = os.environ.get("DB_SCHEMA", default="sfim")

domain_name = os.environ.get("SFIM_DOMAIN_NAME", default="sfim.tools")

api_key = os.environ.get("MAILGUN_API_KEY", default="f78072e3f56aaf15777d985a378e1e30-074fa10c-6fb8ecef")