from flask import render_template, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html', title='Gestion Route', cur=current_user)


@main.route('/about')
def about():
    return render_template('about.html', title='About')

