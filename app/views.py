from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
	return render_template('home.html')

@views.route('/results')
def results():
	return render_template('results.html')

@views.route('/create-poll', methods=['GET', 'POST'])
def create_poll():
	return render_template('create-poll.html')

@views.route('/vote')
def vote():
	return render_template('vote.html')

@views.route('/poll/<id>')
def poll(id):
	# return f'Poll {id}'
	return render_template('poll.html', id=id)