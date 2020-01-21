from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from models import  Poll

polls = Blueprint('polls', __name__, template_folder='templates', url_prefix='/polls')


@polls.route('/create', methods=('GET', 'POST'))
@login_required
def create_poll():
    if request.method == 'POST':
        return '1'

    return render_template('create_poll.html')


@polls.route('/<int:poll_id>', methods=('GET', 'POST'))
@login_required
def take_poll(poll_id):
    poll = Poll.query.get(poll_id)

    if request.method == 'POST':
        data = request.get_json()
        poll.complete_poll(data, current_user.id)
        return 'Successfully stored'

    return render_template('take_poll.html', data=poll.get_json())


@polls.route('/view/<int:poll_id>')
def view_poll(poll_id):
    poll = Poll.query.get(poll_id)

    return render_template('view_poll.html', data=poll.aggregate_results())

