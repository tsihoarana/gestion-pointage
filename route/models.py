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
    points = db.relationship('Pointage', backref='employe', lazy=True)
    def __repr__(self):
        return f"User('{self.nom}')"

class Categorie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), unique=True, nullable=False)
    heure_hebdo = db.Column(db.Integer, nullable=False)
    salaire_hebdo = db.Column(db.Numeric(15,3), nullable=False)
    indemnite = db.Column(db.Numeric(15,3), nullable=False)
    liste_jour = db.Column(db.String(100), nullable=False)
    users = db.relationship('User', backref='cat', lazy=True)
    def __repr__(self):
        return f"{self.nom}"

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cle = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    valeur = db.Column(db.Numeric(16,3), nullable=False)

class Pointage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    iduser = db.Column(db.Integer, db.ForeignKey('user.id'))

class Detailpointage(db.Model):
    # __table_args__ = (
    #     db.CheckConstraint('heure_jour >= 0'),
    #     db.CheckConstraint('heure_nuit >= 0'),
    # )
    id = db.Column(db.Integer, primary_key=True)
    idpointage = db.Column(db.Integer, db.ForeignKey('pointage.id'))
    jour = db.Column(db.String(20), nullable=False)
    est_ferier = db.Column(db.Float, nullable=False)
    heure_jour = db.Column(db.Float, nullable=False)
    heure_nuit = db.Column(db.Float, nullable=False)
