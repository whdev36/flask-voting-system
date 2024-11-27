from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .forms import PollForm
from .models import Option, Poll

views = Blueprint('views', __name__)

@views.route('/')
def home():
	return render_template('home.html')

@views.route('/results')
def results():
	return render_template('results.html')

@views.route('/create-poll', methods=['GET', 'POST'])
def create_poll():
	form = PollForm()
	if form.validate_on_submit():
		poll = Poll(question=form.question.data)
		db.session.add(poll)
		db.session.commit()
		for option_form in form.options:
			option = Option(text=option_form.text.data, poll_id=poll.id)
			db.session.add(option)
		db.session.commit()
		flash('Poll successfully created!', 'success')
		return redirect(url_for('home'))
	return render_template('create-poll.html', form=form)

@views.route('/vote')
def vote():
	return render_template('vote.html')