import bcrypt
from flask import Blueprint, render_template, url_for, redirect, flash
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from app import db

auth = Blueprint('auth', __name__, template_folder='templates', url_prefix='/auth')


# TODO: Use Bcrypt

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    # If POST request
    if form.validate_on_submit():
        if User.query.filter(User.username == form.username.data).first():
            user = User.query.filter(User.username == form.username.data).first()

            if bcrypt.checkpw(form.password.data.encode(),
                              user.password.encode()):
                login_user(user)
                return redirect(url_for('index'))

        flash('Wrong username or password', 'error')
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    # If POST request
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user:
            flash('This username is taken...', 'error')
            return redirect(url_for('auth.register'))

        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)

        new_user = User(username=username, password=hashed)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('registration.html', form=form)
