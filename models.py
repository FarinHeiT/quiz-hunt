from app import db
import re


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))


    def __repr__(self):
        return ''.format(self.id)
