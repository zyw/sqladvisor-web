from flask import Flask,render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'

def create_app(config_name):
	app = Flask(__name__)
 	app.config.from_object(config[config_name])
 	config[config_name].init_app(app)

 	db.init_app(app)
 	login_manager.init_app(app)

 	from .main import main as main_blueprint
 	app.register_blueprint(main_blueprint)

 	return app