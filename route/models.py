from datetime import datetime
from flask import current_app
from route import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    nom = db.Column(db.String(20), nullable=False)
    prenom = db.Column(db.String(20), nullable=False)
    date_naissance = db.Column(db.DateTime, nullable=False)
    date_embauche = db.Column(db.DateTime, nullable=False)
    date_fin_contrat = db.Column(db.DateTime, nullable=False)
    type_user = db.Column(db.Integer, nullable=False)
    idcategorie = db.Column(db.Integer, db.ForeignKey('categorie.id'))
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.nom}')"

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), unique=True, nullable=False)
    heure_hebdo = db.Column(db.Integer, nullable=False)
    salaire_hebdo = db.Column(db.Numeric(15,3), nullable=False)
    liste_jour = db.Column(db.String(100), unique=True, nullable=False)
