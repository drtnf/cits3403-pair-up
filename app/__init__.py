from flask import Flask
from config import DevelopmentConfig as dev
from config import ProductionConfig as prod
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login.login_manager import LoginManager

app = Flask(__name__)
app.config.from_object(prod)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

#from app import routes,models
from app import routes,models,api,wordle
