from flask import Flask, render_template, send_from_directory
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from auth.auth_bp import auth
app.register_blueprint(auth)



from models import User
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/about')
def about_us():
    return render_template('about.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


from models import Poll


@app.route('/')
def index():
    polls = Poll.query.order_by(Poll.created_date.desc()).all()
    return render_template('main.html', polls=polls)


@app.route('/files/<path:filename>')
def get_file(filename):
    return send_from_directory('files', filename)


if __name__ == '__main__':
    app.run()
