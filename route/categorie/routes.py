from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from route.models import Categorie
from route.categorie.forms import CatForm
from route import db


categorie = Blueprint('categorie', __name__)


@categorie.route('/categorie')
@login_required
def cat():
    page = request.args.get('page', 1, type=int)
    cats = Categorie.query.paginate(page=page, per_page=5)
    return render_template('categorie.html', title='Listes categories', cats=cats)

@categorie.route('/categorie/add', methods=['GET', 'POST'])
@login_required
def add_cat():
    form = CatForm()
    if form.validate_on_submit():
        cat = Categorie(nom=form.nom.data,
                    heure_hebdo=form.heure_hebdo.data,
                    salaire_hebdo=form.salaire_hebdo.data,
                    liste_jour=form.liste_jour.data)
        db.session.add(cat)
        db.session.commit()
        flash(f'Categorie created', 'success')
        return redirect(url_for('categorie.cat'))
    return render_template('categorie_form.html', title='Ajout categorie', form=form)

@categorie.route('/categorie/<int:cat_id>/update', methods=['GET', 'POST'])
@login_required
def updateCat(cat_id):
    cat = Categorie.query.get_or_404(cat_id)
    form = CatForm()
    if form.validate_on_submit():
        cat.nom = form.nom.data
        cat.heure_hebdo = form.heure_hebdo.data
        cat.salaire_hebdo = form.salaire_hebdo.data
        cat.liste_jour = form.liste_jour.data

        db.session.commit()
        flash('Your categorie has been updated!', 'success')
        return redirect(url_for('categorie.cat'))
    else:
        form.nom.data = cat.nom
        form.heure_hebdo.data = cat.heure_hebdo
        form.salaire_hebdo.data = cat.salaire_hebdo
        form.liste_jour.data = cat.liste_jour
    return render_template('categorie_form.html', title='Update employe', form=form, legend='Update employe')

@categorie.route('/categorie/<int:cat_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteCat(cat_id):
    cat = Categorie.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Your categorie has been deleted!', 'success')
    return redirect(url_for('categorie.cat'))