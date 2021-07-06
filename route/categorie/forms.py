from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.widgets import html5 as h5widgets
from wtforms.fields import html5
from flask_login import current_user
from route.models import User, Categorie

class CatForm(FlaskForm):
    nom = StringField('Nom', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    heure_hebdo = IntegerField('Heure Hebdo', 
                            validators=[DataRequired(), NumberRange(min=1)],
                            widget=h5widgets.NumberInput(min=1))
    salaire_hebdo = DecimalField('Salaire Hebdo', validators=[DataRequired(), NumberRange(min=1)])
    indemnite = DecimalField('Indemnite', validators=[DataRequired(), NumberRange(min=0)])
    liste_jour = StringField('Liste Jour', 
                            validators=[DataRequired()])

    submit = SubmitField('Ajouter')
