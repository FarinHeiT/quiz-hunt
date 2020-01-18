from flask import Blueprint, render_template, url_for, redirect, flash, jsonify
from models import  Poll

polls = Blueprint('polls', __name__, template_folder='templates', url_prefix='/polls')


@polls.route('/<int:poll_id>')
def take_poll(poll_id):
    poll = Poll.query.get(poll_id)
    return render_template('take_poll.html', data=poll.get_json())