from app import app
from flask import render_template

@app.route('/')
def index():
    return 'works'

if __name__ == '__main__':
    app.run()
