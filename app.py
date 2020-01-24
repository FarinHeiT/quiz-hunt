from flask import Flask, render_template, send_from_directory, redirect, url_for, escape
from flask_login import LoginManager, current_user, login_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from auth.forms import SuggestForm, ChatForm
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_socketio import SocketIO, send, emit
import jinja2

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app)

# TODO Polls creationg and walkthrough form validation using wtforms

admin = Admin(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# noinspection PyPep8
from auth.auth_bp import auth
from polls.polls_bp import polls

app.register_blueprint(auth)
app.register_blueprint(polls)

from models import User, Suggestion

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'


@app.route('/suggest', methods=['GET', 'POST'])
@login_required
def suggest():
    form = SuggestForm()
    if form.validate_on_submit():
        message = form.text.data
        topic = form.topic.data
        class_message = Suggestion(message=message, author_id=current_user.id, topic=topic)
        db.session.add(class_message)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('suggestions.html', form=form)


@app.route('/about')
def about_us():
    return render_template('about.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# add admin pages here
from models import *

admin.add_view(ModelView(Poll, db.session))
admin.add_view(ModelView(Suggestion, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(MsgHistory, db.session))


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = ChatForm()
    messages = MsgHistory.query.all()
    return render_template('chat.html', messages=messages, form=form)


def messageRecived():
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    message = MsgHistory(message=json['message'], user=current_user.username)
    db.session.add(message)
    db.session.commit()
    json['message'] = str(escape(json['message']))
    socketio.emit('my response', json, callback=messageRecived)


# flask-security
# user_datascore = SQLAlchemySessionUserDatastore(db.session, User, Role)
# security = Security(app, user_datascore)

@app.route('/')
def index():
    polls = Poll.query.order_by(Poll.created_date.desc()).all()
    return render_template('main.html', polls=polls)


@app.route('/files/<path:filename>')
def get_file(filename):
    return send_from_directory('files', filename)


@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html')


if __name__ == '__main__':
    socketio.run(app)
