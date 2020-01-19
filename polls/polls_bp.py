from flask import Blueprint, render_template, url_for, redirect, flash, jsonify, request
from flask_login import current_user
from models import  Poll

polls = Blueprint('polls', __name__, template_folder='templates', url_prefix='/polls')


@polls.route('/<int:poll_id>', methods=('GET', 'POST'))
def take_poll(poll_id):
    poll = Poll.query.get(poll_id)

    if request.method == 'POST':
        data = request.get_json()
        poll.complete_poll(data, current_user.id)

        return 'ok'
    return render_template('take_poll.html', data=poll.get_json())