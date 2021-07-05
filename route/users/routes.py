from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from route import db, bcrypt
from route.models import User
from route.users.forms import RegistrationForm, LoginForm, UpdateForm
import route.users.utils as utils

users = Blueprint('users', __name__)


@users.route('/user')
@login_required
def user():
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=5)
    return render_template('user.html', title='Listes user', users=users, utils=utils)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(matricule=form.matricule.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(matricule=form.matricule.data,
                    nom=form.nom.data,
                    prenom=form.prenom.data,
                    date_naissance=form.date_naissance.data,
                    date_embauche=form.date_embauche.data,
                    date_fin_contrat=form.date_fin_contrat.data,
                    type_user=form.type_user.data,
                    idcategorie=form.idcategorie.data.id,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.nom.data}', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

@users.route('/user/<int:user_id>/update', methods=['GET', 'POST'])
@login_required
def updateUser(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.nom = form.nom.data
        user.prenom = form.prenom.data
        user.date_naissance = form.date_naissance.data
        user.date_embauche = form.date_embauche.data
        user.date_fin_contrat = form.date_fin_contrat.data
        user.type_user = form.type_user.data
        user.idcategorie = form.idcategorie.data.id
        user.password = hashed_password

        db.session.commit()
        flash('Your portion has been updated!', 'success')
        return redirect(url_for('users.user'))
    else:
        form.matricule.data = user.matricule
        form.nom.data = user.nom
        form.prenom.data = user.prenom
        form.date_naissance.data = user.date_naissance
        form.date_embauche.data = user.date_embauche
        form.date_fin_contrat.data = user.date_fin_contrat
        form.type_user.data = user.type_user
        form.idcategorie.data = user.idcategorie
    return render_template('register.html', title='Update employe', form=form, legend='Update employe')