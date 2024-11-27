from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), nullable=False)
	first_name = db.Column(db.String(30), nullable=False, unique=True)
	last_name = db.Column(db.String(30), nullable=False)
	password = db.Column(db.String(100), nullable=False)
	votes = db.relationship('Vote', backref='user', lazy=True)

	def __repr__(self):
		return '<User %r>' % self.email

class Poll(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(255), nullable=False)
	created_at = db.Column(db.DateTime, default=func.now())
	options = db.relationship('Option', backref='poll', lazy=True)
	votes = db.relationship('Vote', backref='poll', lazy=True)


	def __repr__(self):
		return '<Poll %r>' % self.question

class Option(db.Model):
	id = db.Column(db.Integer)
	text = db.Column(db.String(255), nullable=False)
	poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
	votes = db.relationship('Vote', backref='option', lazy=True)

	def __repr__(self):
		return '<Option %r>' % self.text

class Vote(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
	option_id = db.Column(db.Integer, db.ForeignKey('option.id'), nullable=False)
	created_at = db.Column(db.DateTime, default=func.now())

	def __repr__(self):
		return '<Vote %r>' % self.user_id