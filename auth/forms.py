from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, EqualTo, InputRequired, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    button = SubmitField(label='Login')


class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])

    password = PasswordField('New Password',
                             validators=[InputRequired(),
                                         EqualTo('password_again',
                                                 message='Passwords must match!'),
                                         Length(8, 128, message='Minimal password length: 8 characters')
                                         ])

    password_again = PasswordField('Repeat Password')
    button = SubmitField(label='Login')


class SuggestForm(FlaskForm):
    text = StringField('text', validators=[DataRequired()])
    button = SubmitField(label='Submit')
    topic = SelectField('Topic', choices=[('Error', 'Error'), ('Suggest', 'Suggest'), ('rate', 'rate')])


class ChatForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    text = StringField('text', validators=[DataRequired()])
    button = SubmitField(label='Send')
