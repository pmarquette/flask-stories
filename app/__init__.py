from flask import Flask
from config import Config
from mongoengine import *
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)
connect('project1', host=Config.DATABASE_URI)
login = LoginManager(app)
login.login_view = 'auth.login'
mail = Mail(app)

from app import routes

from app.auth import blueprint as auth_blueprint
from app.api import blueprint as api_blueprint
app.register_blueprint(auth_blueprint)
app.register_blueprint(api_blueprint, url_prefix='/api')