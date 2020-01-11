from app import db
from flask_login import UserMixin


class User(db.Model,  UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))

    def __repr__(self):
        return f'User: {self.username}'
