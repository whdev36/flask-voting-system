from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import PollForm, OptionForm
from .models import Poll, Option
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
	polls = Poll.query.all()
	return render_template('home.html', polls=polls)

@views.route('/results')
def results():
	return render_template('results.html')

@views.route('/create-poll', methods=['GET', 'POST'])
@login_required
def create_poll():
	form = PollForm()
	if form.validate_on_submit():
		# Poll saving
		poll = Poll(question=form.question.data, user_id=current_user.id)
		db.session.add(poll)
		db.session.commit() # Save poll

		# Saving option
		for option_form in form.options:
			option = Option(text=option_form.text.data, poll_id=poll.id)
			db.session.add(option)
		db.session.commit()

		flash('Poll successfully created!', 'success')
		return redirect(url_for('views.home'))
	else:
		print(form.errors) # Check form errors
	return render_template('create-poll.html', form=form)

@views.route('/vote')
def vote():
	return render_template('vote.html')

@views.route('/poll/<id>')
def poll(id):
	# return f'Poll {id}'
	return render_template('poll.html', id=id)