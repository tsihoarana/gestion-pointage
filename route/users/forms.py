from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from wtforms.widgets import html5 as h5widgets
# from wtforms.fields import html5
from flask_login import current_user
from route.models import User


class RegistrationForm(FlaskForm):
    matricule = StringField('Matricule', 
                            validators=[DataRequired(), Length(min=2 , max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    # type = StringField('privilege', validators=[DataRequired()])
    type = SelectField('type', choices=[('0', 'Admin'), ('1', 'Normal')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one')


    
class LoginForm(FlaskForm):
    matricule = StringField('Matricule', 
                            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


