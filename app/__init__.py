from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_cors import CORS
from flask_restful import Api
from . import config
import os

# Configure objects
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
	app = Flask(__name__)

	# Add configuration settings
	app.config.from_object(config.Config)

	# Add Flask extensions
	db.init_app(app)
	migrate.init_app(app)
	login_manager.init_app(app)
	CORS(app)

	# Login manager settings
	from .models import User

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	login_manager.login_view = 'auth.login'
	login_manager.login_message = 'Please log in to access this page.'

	# Register blueprint
	from .views import views
	from .auth import auth

	app.register_blueprint(views)
	app.register_blueprint(auth)

	# Check directory and create database
	db_name = config.Config.DATABASE_NAME
	if not os.path.exists(db_name):
		with app.app_context():
			db.create_all()
		print(f'{db_name} created successfully!')

	return app