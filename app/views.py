from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .forms import PollForm
from .models import Option, Poll
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
def create_poll():
	form = PollForm()
	if form.validate_on_submit():
		try:
			poll = Poll(question=form.question.data)
			db.session.add(poll)
			db.session.commit()
			if form.option_1.data.strip():
				db.session.add(Option(text=form.option_1.data, poll_id=poll.id))
			if form.option_2.data.strip():
				db.session.add(Option(text=form.option_2.data, poll_id=poll.id))
			if form.option_3.data.strip():
				db.session.add(Option(text=form.option_4.data, poll_id=poll.id))
			if form.option_4.data.strip():
				db.session.add(Option(text=form.option_4.data, poll_id=poll.id))
			db.session.commit()
			flash('Poll successfully created!', 'success')
			return redirect(url_for('views.home'))
		except Exception as e:
			db.session.rollback()
			flash(f'Error: {str(e)}', 'danger')
	return render_template('create-poll.html', form=form)

@views.route('/vote')
def vote():
	return render_template('vote.html')

@views.route('/poll/<id>')
def poll(id):
	# return f'Poll {id}'
	return render_template('poll.html', id=id)