from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from .models import User

class RegisterForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
	last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			ValidationError('This email is already in use. Please choose a different one.')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class OptionForm(FlaskForm):
	text = StringField('Option', validators=[DataRequired()])

class PollForm(FlaskForm):
	question = TextAreaField('Poll Question', validators=[DataRequired(), Length(max=255)])
	options = FieldList(FormField(OptionForm), min_entries=2, max_entries=10)
	submit = SubmitField('Create')

# Voting Form
class VoteForm(FlaskForm):
	option = SelectField('Choose an Option', coerce=int, validators=[DataRequired()])
	submit = SubmitField('Vote')