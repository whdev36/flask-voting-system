from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), nullable=False, unique=True)
	first_name = db.Column(db.String(30), nullable=False)
	last_name = db.Column(db.String(30), nullable=False)
	password = db.Column(db.String(255), nullable=False)

	def __repr__(self):
		return '<User %r>' % self.email

class Poll(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	question = db.Column(db.String(255), nullable=False)
	created_at = db.Column(db.DateTime(timezone=True), default=func.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	options = db.relationship('Option', backref='poll', lazy=True)


	def __repr__(self):
		return '<Poll %r>' % self.question

class Option(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text = db.Column(db.String(255), nullable=False)
	votes = db.Column(db.Integer, default=0)
	poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)

	def __repr__(self):
		return '<Option %r>' % self.text