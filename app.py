from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:\\Users\\18122\\PycharmProjects\\Quiz-Hunt\\Maindb.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
