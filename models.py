from app import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    polls = db.relationship('Poll', backref='author', lazy=True)
    completed_polls = db.relationship('CompletedPoll', backref='completed_by', lazy=True)

    def __repr__(self):
        return f'User: {self.username}'


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120), unique=True)
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    questions = db.relationship('Question', backref='poll', lazy=True)



    def __repr__(self):
        return f'Poll: {self.title}'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    text = db.Column(db.String(120))
    question_no = db.Column(db.Integer)
    answer_options = db.relationship('AnswerOption', backref='question', lazy=True)

    def __repr__(self):
        return f'Question: {self.text}'


class AnswerOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    text = db.Column(db.String(120))

    def __repr__(self):
        return f'AnswerOption: {self.text}'


class CompletedPoll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    answered_questions = db.relationship('AnsweredQuestion', backref='completed_poll', lazy=True)

    def __repr__(self):
        return f'CompletedPoll id: {self.poll_id}. Author: {self.author_id}'


class AnsweredQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completedpoll_id = db.Column(db.Integer, db.ForeignKey('completed_poll.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', backref='answered_question', lazy=True)
    answer_id = db.Column(db.Integer, db.ForeignKey('answer_option.id'))
    answer_option = db.relationship('AnswerOption', backref='answered_option', lazy=True)

    def __repr__(self):
        return f'Question: {self.question} ' \
               f'Answer: {self.answer_option.text}'