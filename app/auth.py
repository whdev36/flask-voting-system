from flask import Blueprint, render_template, flash, redirect, url_for
from .forms import RegisterForm
from .models import User
from . import db
from werkzeug.security import generate_password_hash,  check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
	return render_template('login.html')

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
		return redirect(url_for('login'))
	return render_template('register.html')

@auth.route('/logout')
def logout():
	return 'Logout'