import os

class Config:
	DEBUG = True
	DATABASE_NAME = 'vote.db'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_NAME
	SQLALCHEMY_TRACK_MODIFIACATIONS = False
	SECRET_KEY = os.environ.get('SECRET_KEY', 'DEFAULT_SECRET_KEY')
	ADMIN_NAME = 'OVS'
	ADMIN_TEMPLATE_MODE = 'bootstrap4'
	ADMIN_ALLOWED_EMAILS = ['admin@example.com']