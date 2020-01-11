from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///Maindb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
