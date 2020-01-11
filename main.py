from app import app
from flask import render_template

from auth.auth_bp import auth
app.register_blueprint(auth)


@app.route('/')
def index():
    return render_template('main.html')

if __name__ == '__main__':
    app.run()
