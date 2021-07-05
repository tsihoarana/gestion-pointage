from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from route.models import Pointage, Detailpointage, User
# from route.pointage.forms import CatForm
from route import db
from route.config import Default
from route.pointage import services


pointage = Blueprint('pointage', __name__)


@pointage.route('/pointage', methods=['GET', 'POST'])
@login_required
def add_pointage():
    days = Default.DAYS
    return render_template('pointage.html', title='Listes categories', days=days)

@pointage.route('/pointage/<int:user_id>')
@login_required
def insert_pointage(user_id):
    days = Default.DAYS
    ferie = {}
    jour = {}
    nuit = {}
    for day in days:
        ferie[day] = 0
    for key in request.form:
        name, typ = key.split("_")
        if typ == 'ferie':
            ferie[name] = 1
        if typ == 'jour':
            jour[name] = request.form.get(key)
        if typ == 'nuit':
            nuit[name] = request.form.get(key)
    services.insertdb_pointage(user_id, ferie, jour, nuit)
    return redirect(url_for('users.user'))

@pointage.route('/pointage/<int:user_id>/calcul')
@login_required
def calcul_heure(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('heure_semaine.html', title="Calcul heure", user=user)