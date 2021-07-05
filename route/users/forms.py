from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.widgets import html5 as h5widgets
from wtforms.fields import html5
from flask_login import current_user
from route.models import User, Categorie


class RegistrationForm(FlaskForm):
    matricule = StringField('Matricule', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    nom = StringField('Nom', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    prenom = StringField('Prenom', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    date_naissance = html5.DateField('Date Naissance', 
                            validators=[DataRequired()])
    date_embauche = html5.DateField('Date Embauche', 
                            validators=[DataRequired()])
    date_fin_contrat = html5.DateField('Date Fin Contrat', 
                            validators=[DataRequired()])

    type_user = SelectField('type', choices=[('1', 'Admin'), ('0', 'Normal')])
    idcategorie = QuerySelectField('Categorie', query_factory=lambda: Categorie.query.all())
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_matricule(self, matricule):
        user = User.query.filter_by(matricule=matricule.data).first()
        if user:
            raise ValidationError('That matricule is taken. Please choose a different one')

class UpdateForm(FlaskForm):
    matricule = StringField('Matricule', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    nom = StringField('Nom', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    prenom = StringField('Prenom', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    date_naissance = html5.DateField('Date Naissance', 
                            validators=[DataRequired()])
    date_embauche = html5.DateField('Date Embauche', 
                            validators=[DataRequired()])
    date_fin_contrat = html5.DateField('Date Fin Contrat', 
                            validators=[DataRequired()])

    type_user = SelectField('type', choices=[('1', 'Admin'), ('0', 'Normal')])
    idcategorie = QuerySelectField('Categorie', query_factory=lambda: Categorie.query.all())
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    

    
class LoginForm(FlaskForm):
    matricule = StringField('Matricule', 
                            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


