from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
	return render_template('home.html')

@views.route('/results')
def results():
	return render_template('results.html')

@views.route('/create-poll')
def create_poll():
	return render_template('create-poll.html')

@views.route('/vote')
def vote():
	return render_template('vote.html')