from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from route.models import Pointage, Detailpointage, User
# from route.pointage.forms import CatForm
from route import db
from route.config import Default
from route.pointage import services


pointage = Blueprint('pointage', __name__)

@pointage.route('/pointage/list', methods=['GET', 'POST'])
@login_required
def list_pointage():
    page = request.args.get('page', 1, type=int)
    points = Pointage.query.paginate(page=page, per_page=5)
    return render_template('list_pointage.html', title='Listes pointages', points=points)



@pointage.route('/pointage', methods=['GET', 'POST'])
@login_required
def add_pointage():
    days = Default.DAYS
    return render_template('pointage.html', title='Listes categories', days=days)

@pointage.route('/pointage/<int:user_id>', methods=['GET', 'POST'])
@login_required
def insert_pointage(user_id):
    days = Default.DAYS
    ferie = {}
    jour = {}
    nuit = {}
    for key in request.form:
        name, typ = key.split("_")
        if typ == 'ferie':
            ferie[name] = request.form.get(key)
        if typ == 'jour':
            jour[name] = request.form.get(key)
        if typ == 'nuit':
            nuit[name] = request.form.get(key)
    pointage_id = services.insertdb_pointage(user_id, ferie, jour, nuit)
    return redirect(url_for('pointage.calcul_heure', user_id=user_id, pointage_id=pointage_id))

@pointage.route('/pointage/<int:user_id>/calcul/<int:pointage_id>', methods=['GET', 'POST'])
@login_required
def calcul_heure(user_id, pointage_id):
    user = User.query.get_or_404(user_id)
    pointage = Pointage.query.get_or_404(pointage_id)
    res = services.calcul_heure(user, pointage)
    return render_template('heure_semaine.html', title="Calcul heure", user=user, results=res, pointage=pointage)

@pointage.route('/pointage/<int:user_id>/fiche-de-paie/<int:pointage_id>', methods=['GET', 'POST'])
@login_required
def fiche_paie(user_id, pointage_id):
    user = User.query.get_or_404(user_id)
    pointage = Pointage.query.get_or_404(pointage_id)
    paie, indemnite, total_paye = services.fiche_de_paie(user, pointage)
    # return render_template('home.html')
    return render_template('fiche_paie.html', title="Fiche de paie", user=user, results=paie,
                                            indemnite=indemnite, total_paye=total_paye)
