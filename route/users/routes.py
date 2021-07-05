from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from route import db, bcrypt
from route.models import User
from route.users.forms import RegistrationForm, LoginForm
from route.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route('/user')
def user():
    users = User.query.all()
    return render_template('user.html', title='Listes user', users=users)


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
