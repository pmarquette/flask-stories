import os
import config_dev

class Config(object):
  SECRET_KEY = os.environ.get('SECRET_KEY') or config_dev.SECRET_KEY
  MAIL_SERVER = os.environ.get('MAIL_SERVER') or config_dev.MAIL_SERVER
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
  MAIL_USE_TLS = 1
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or config_dev.MAIL_USERNAME
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or config_dev.MAIL_PASSWORD
  DATABASE_URI = config_dev.DATABASE_URI