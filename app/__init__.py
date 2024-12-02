from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # SQLite3 database
from flask_login import LoginManager, current_user # User authentication
from flask_migrate import Migrate # Database migrations
from flask_cors import CORS # API CORS
from flask_restful import Api # API
from flask_admin import Admin # Admin
from flask_wtf.csrf import CSRFProtect # CSRF token protection
from flask_login import AnonymousUserMixin # Anonymous User Mixin
from flask_bootstrap import Bootstrap # Bootstrap
from flask_admin.contrib.sqla import ModelView # Admin model view
from . import config # All configurations
import os # Operting system

# Configure objects
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
bootstrap = Bootstrap()

# Create admin model view
class AdminModelView(ModelView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.email in config.Config.ADMIN_ALLOWED_EMAILS

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('auth.login'))

class Anonymous(AnonymousUserMixin):
	id = None # Set none value to user id

def create_app():
	app = Flask(__name__)

	# Add configuration settings
	app.config.from_object(config.Config)

	# Add Flask extensions
	db.init_app(app)
	migrate.init_app(app)
	login_manager.init_app(app)
	csrf.init_app(app)
	bootstrap.init_app(app)
	CORS(app)

	# Login manager settings
	from .models import User, Poll, Option
	from .views import views
	from .auth import auth

	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	login_manager.login_view = 'auth.login' # Set default login page
	login_manager.login_message = 'Please log in to access this page.' # Create default login message
	login_manager.ananymous_user = Anonymous # Set ananymous class

	# Create admin page
	admin = Admin(app, name=config.Config.ADMIN_NAME,
		template_mode=config.Config.ADMIN_TEMPLATE_MODE)
	with app.app_context():
		admin.add_view(AdminModelView(User, db.session))
		admin.add_view(AdminModelView(Poll, db.session))
		admin.add_view(AdminModelView(Option, db.session))

	# Register blueprint
	app.register_blueprint(views)
	app.register_blueprint(auth)

	# Check directory and create database
	db_name = config.Config.DATABASE_NAME
	if not os.path.exists(db_name):
		with app.app_context():
			db.create_all()
		print(f'{db_name} created successfully!')

	return app