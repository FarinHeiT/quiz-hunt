import bcrypt
import click
from flask import Flask, render_template, send_from_directory, redirect, url_for, escape, request
from flask_login import LoginManager, login_required
from flask_security import current_user, roles_required, roles_accepted
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from auth.forms import SuggestForm, ChatForm, SearchForm
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, Security
from flask_socketio import SocketIO
import urllib.parse
from config import Config
from flask_admin.contrib import rediscli
from redis import Redis

app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app)

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

class AdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    column_searchable_list = ['id']


class PollAdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    column_searchable_list = ['title', 'id']
    column_filters = ('title', 'created_date', 'author_id', 'description', 'id')

class MsgAdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    column_searchable_list = ['id', 'user', 'message']
    column_filters = ('id', 'user', 'message', 'id')


class SuggestionsAdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    column_searchable_list = ['id', 'author_id', 'topic']
    column_filters = ('id', 'author_id', 'topic', 'id')


class UserAdminView(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    column_searchable_list = ['username', 'id']
    column_filters = ('id','username', 'active', 'polls', 'completed_polls', 'roles')





class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

    @expose('/')
    def index(self):
        return self.render(name="home", template="admin_home.html", url="/admin", msghistory=MsgHistory.query.count(),
                           users=User.query.count(), polls=Poll.query.count(), suggest=Suggestion.query.count(),
                           completedpolls=CompletedPoll.query.count())




''' to make a admin'''
#from app import db
#from app import user_datastore
#from models import *
#mq = User.query.all()
#user = mq[user number that you want to make admin]
#role = Role.query.first()
#user_datastore.add_role_to_user(user, role)
#b.session.commit()

admin = Admin(app, 'Quiz-Hunt', url='/', index_view=HomeAdminView())
admin.add_view(PollAdminView(Poll, db.session))
admin.add_view(SuggestionsAdminView(Suggestion, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(MsgAdminView(MsgHistory, db.session))
admin.add_view(AdminView(CompletedPoll, db.session))
#admin.add_view(rediscli.RedisCli(Redis()))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    form = ChatForm()
    messages = MsgHistory.query.all()
    amount = MsgHistory.query.count()
    if amount > 99:
        MsgHistory.query.delete()
        db.session.commit()
    return render_template('chat.html', messages=messages, form=form)


def messageRecived():
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    # URI Decoding and Length restriction
    json['message'] = urllib.parse.unquote(json['message'])[:237]

    message = MsgHistory(message=json['message'], user=current_user.username)
    db.session.add(message)
    db.session.commit()
    json['message'] = str(escape(json['message']))
    socketio.emit('my response', json, callback=messageRecived)


@app.route('/')
def index():
    form = SearchForm()
    q = request.args.get('q')
    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    if q:
        polls = Poll.query.filter(Poll.title.contains(q) | Poll.description.contains(q))
    else:
        polls = Poll.query.order_by(Poll.created_date.desc())

    pages = polls.paginate(page=page, per_page=6)

    return render_template('main.html', polls=polls, pages=pages)


@app.route('/files/<path:filename>')
def get_file(filename):
    return send_from_directory('files', filename)


@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html'), 404


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403


@app.errorhandler(500)
def forbidden(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    socketio.run(app)


# CLI Helper methods
@app.cli.command('create-user')
@click.option('-u', '--username', required=True)
@click.option('-p', '--password', required=True)
@click.option('-a', '--admin', default=0)
@click.option('--active', default=1)
def create_user(username, password, admin, active):
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)

        new_user = User(username=username, password=hashed, active=active)

        if admin:
            admin_role = Role.query.filter(Role.name == 'admin').first()
            user_datastore.add_role_to_user(new_user, admin_role)

        db.session.add(new_user)
        db.session.commit()
        print(f'Created user: {username}')
    except Exception as e:
        print('Something went wrong: ', e)


app.cli.add_command(create_user)
