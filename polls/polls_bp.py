import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import current_user, login_required
from models import Poll, CompletedPoll
from .validation import validate_creation, validate_taking
from werkzeug.utils import secure_filename
from app import db
from config import Config

polls = Blueprint('polls', __name__, template_folder='templates', url_prefix='/polls')


@polls.route('/create', methods=('GET', 'POST'))
@login_required
def create_poll():
    if request.method == 'POST':
        data = request.get_json()

        # Data validation
        if validate_creation(data):
            # If there is no poll with given name
            poll = Poll.query.filter(Poll.title == data['title']).first()
            if not poll:
                new_poll = current_user.create_poll(**data)
                return {'status': "Success"}
            else:
                return {'status': "TitleAlreadyExists"}
        else:
            return {'status': 'ValidationError'}

    return render_template('create_poll.html')


@polls.route('/<int:poll_id>', methods=('GET', 'POST'))
@login_required
def take_poll(poll_id):
    completed_poll = db.session.query(CompletedPoll) \
        .filter(CompletedPoll.poll_id == poll_id,
                CompletedPoll.author_id == current_user.id).first()

    # If this user have already completed this poll
    if completed_poll:
        return abort(403)

    poll = Poll.query.get(poll_id)
    if request.method == 'POST':
        data = request.get_json()

        if validate_taking(data, poll.get_json()):
            poll.complete_poll(data, current_user.id)
            return {'status': "Success"}
        else:
            return {'status': 'ValidationError'}

    return render_template('take_poll.html', data=poll.get_json())


@polls.route('/view/<int:poll_id>')
def view_poll(poll_id):

    completed_poll = db.session.query(CompletedPoll) \
        .filter(CompletedPoll.poll_id == poll_id,
                CompletedPoll.author_id == current_user.id).first()

    # If this user haven't completed this poll
    if not completed_poll:
        return abort(403)

    poll = Poll.query.get(poll_id)

    return render_template('view_poll.html', data=poll.aggregate_results())


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@polls.route('/image_upload', methods=['POST', ])
def image_upload():
    if 'file' not in request.files:
        return {'status': 'A file must be selected'}

    file = request.files['file']

    if file.filename == '':
        return {'status': 'A file must be selected'}

    if file and allowed_file(file.filename):
        filename = secure_filename(current_user.username + str(time.time()).split('.')[1])
        file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        return {'status': 'Success', 'filename': filename}
