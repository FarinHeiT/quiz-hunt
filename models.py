from app import db
from datetime import datetime
from flask_security import UserMixin
from sqlalchemy import func
from flask_security import RoleMixin

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
                       )

class MsgHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column('message', db.String(500))
    user = db.Column('user', db.String(200))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))
    polls = db.relationship('Poll', backref='author', lazy=True)
    completed_polls = db.relationship('CompletedPoll', backref='completed_by', lazy=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Boolean())

    def create_poll(self, questions, title, description='', filename='poll.jpg'):
        """ Creates new poll with given Q, Qno and answer options {'q1': (1, [a, b])} """

        new_poll = Poll(author_id=self.id,
                        title=title,
                        image_name=filename,
                        description=description)

        # q: question, options: answer options
        for q, options in questions.items():
            answer_options = options

            # Get newly created question
            question = new_poll.create_question(q)

            for option in answer_options:
                question.create_ans_opt(option)

        self.polls.append(new_poll)
        db.session.commit()
        return new_poll

    def __repr__(self):
        return f'User: {self.username}'


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120), unique=True)
    image_name = db.Column(db.String(120), default='poll.jpg')
    description = db.Column(db.Text(400))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    questions = db.relationship('Question', backref='poll', lazy='dynamic')

    def create_question(self, text):
        """ Creates question to the parent poll """
        new_question = Question(poll_id=self.id,
                                text=text)

        self.questions.append(new_question)
        return new_question

    def get_json(self):
        """ Return JSON serialized poll """
        data = {}
        for question in self.questions:
            answer_options = [(answer_option.text, answer_option.id)
                              for answer_option in question.answer_options]
            data[question.text] = answer_options
        return data

    def complete_poll(self, data, author_id):
        """ Writes the answer data to DB """

        completed_poll = CompletedPoll(poll_id=self.id,
                                       author_id=author_id)
        db.session.flush()

        for answer in data.items():
            question_id = self.questions.filter(Question.text == answer[0]).first().id
            answered_question = AnsweredQuestion(completedpoll_id=completed_poll.id,
                                                 question_id=question_id,
                                                 answer_id=answer[1]
                                                 )
            completed_poll.answered_questions.append(answered_question)

        db.session.add(completed_poll)
        db.session.commit()

    def aggregate_results(self):
        completed_polls = CompletedPoll.query.filter(CompletedPoll.poll_id == self.id).all()
        questions = [q.text for q in self.questions.all()]
        answer_options = []
        counts = []
        for question in self.questions:
            answer_options.append([answer_option.text
                                   for answer_option in question.answer_options])

        for question in self.questions.all():
            r = db.session.query(AnsweredQuestion.answer_id, func.count(AnsweredQuestion.answer_id)) \
                .group_by(AnsweredQuestion.answer_id) \
                .filter(AnsweredQuestion.question.has(Question.poll_id == self.id),
                        AnsweredQuestion.question_id == question.id).all()
            counts.append([data[1] for data in r])

        return list(zip(questions, answer_options, counts))

    def __repr__(self):
        return f'Poll: {self.title}'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    text = db.Column(db.String(120))
    answer_options = db.relationship('AnswerOption', backref='question', lazy=True)

    def create_ans_opt(self, text):
        """ Creates answer option to the parent question """
        new_ans_opt = AnswerOption(question_id=self.id,
                                   text=text)

        self.answer_options.append(new_ans_opt)

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


class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(1000))
    author_id = db.Column(db.Integer)
    topic = db.Column(db.String(200))

    def __repr__(self):
        return f'User: {self.author_id}'
