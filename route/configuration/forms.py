from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.widgets import html5 as h5widgets
from wtforms.fields import html5
from flask_login import current_user
from route.models import User, Categorie, Config

class ConfigForm(FlaskForm):
    cle = StringField('Cle', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    description = StringField('Description', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    valeur = DecimalField('Valeur', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Ajouter')
