from app import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    polls = db.relationship('Poll', backref='author', lazy=True)
    completed_polls = db.relationship('CompletedPoll', backref='completed_by', lazy=True)

    def create_poll(self, title, description, data):
        """ Creates new poll with given Q, Qno and answer options {'q1': (1, [a, b])} """

        new_poll = Poll(author_id=self.id,
                        title=title,
                        image_name='poll.jpg',
                        description=description)

        # q: question, q_no: question number ans_opt: answer options
        for q, options in data.items():
            q_no, answer_options = options

            # Get newly created question
            question = new_poll.create_question(q, q_no)

            for option in answer_options:
                question.create_ans_opt(option)

        self.polls.append(new_poll)
        db.session.commit()

    def __repr__(self):
        return f'User: {self.username}'



class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(120), unique=True)
    image_name = db.Column(db.String(120), default='poll.jpg')
    description = db.Column(db.Text(400))
    created_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    questions = db.relationship('Question', backref='poll', lazy=True)

    def create_question(self, text, question_no):
        """ Creates question to the parent poll """
        new_question = Question(poll_id=self.id,
                                text=text,
                                question_no=question_no)

        self.questions.append(new_question)
        return new_question

    def get_json(self):
        """ Return JSON serialized poll """
        data = {}
        for question in self.questions:
            answer_options = [(answer_option.text, answer_option.id)
                              for answer_option in question.answer_options]
            data[question.text] = (question.question_no, answer_options)
        return data

    def __repr__(self):
        return f'Poll: {self.title}'


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    text = db.Column(db.String(120))
    question_no = db.Column(db.Integer)
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
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    topic = db.Column(db.String(200))

    def __repr__(self):
        return f'User: {self.author_id}'
