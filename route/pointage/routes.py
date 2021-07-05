from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
# from route.models import Pointage
# from route.pointage.forms import CatForm
from route import db

pointage = Blueprint('pointage', __name__)


@pointage.route('/pointage/<int:user_id>', methods=['GET', 'POST'])
@login_required
def add_pointage(user_id):
    from route.config import Default
    days = Default.DAYS
    return render_template('pointage.html', title='Listes categories', days=days)

@pointage.route('/pointage', methods=['POST'])
@login_required
def insert_pointage():
    from route.config import Default
    days = Default.DAYS
    ferie = {}
    jour = {}
    nuit = {}
    for day in days:
        ferie[day] = False
    for key in request.form:
        name, typ = key.split("_")
        if typ == 'ferie':
            ferie[name] = True
        if typ == 'jour':
            jour[name] = request.form.get(key)
        if typ == 'nuit':
           nuit[name] = request.form.get(key)
    return render_template('home.html', title='Listes categories', val=ferie)