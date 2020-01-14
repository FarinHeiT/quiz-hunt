from flask import Blueprint, render_template


about = Blueprint('about', __name__, template_folder='../templates', url_prefix='/about')


@about.route('/about')
def about_us():
    return render_template('about.html')
