from flask import Blueprint, render_template, flash, redirect, url_for, request
from .forms import RegisterForm, LoginForm
from .models import User
from . import db
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import login_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and check_password_hash(user.password, form.password.data):
			login_user(user)
			flash('Logged in successfully!', 'success')
			next_page = request.args.get('next')
			return redirect(next) if next_page else redirect(url_for('views.home'))
		else:
			flash('Invalid email or password. Please try again!', 'danger')
	return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(
			email=form.email.data, first_name=form.first_name.data,
			last_name=form.last_name.data,
			password=generate_password_hash(form.password.data))
		db.session.add(user)
		db.session.commit() # SAVE
		flash('Your account has been created! You can now log in.', 'success')
		return redirect(url_for('auth.login'))
	return render_template('register.html', form=form)

@auth.route('/logout')
def logout():
	return 'Logout'