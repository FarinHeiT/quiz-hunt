from app import app
from flask import url_for, render_template

@app.route('/')
def index():
    return url_for('auth.login')

if __name__ == '__main__':
    app.run()
