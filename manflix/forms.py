from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField  
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from manflix.models import UserData

# Form Class For Adding Movie
class AddMovieForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    movie_id_tmd = StringField('TMDB Movie ID', validators=[DataRequired()])
    quality = BooleanField('Quality', default='checked')
    dolby_audio = BooleanField('Dolby Audio', default='checked')
    dual_audio = BooleanField('Dual Audio', default='checked')
    submit = SubmitField('Add Movie')

# Registration Form For User
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = UserData.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username Is Already Taken. Please Use Another Username!')
    def validate_email(self,email):
        user = UserData.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is Already Registered. Log In!')

# Login Form For User
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])   
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# Form Class For Searching Movie
class SearchMovieForm(FlaskForm):
    movie_name = StringField('Search For Movie Movie ID', validators=[DataRequired()])
    submit = SubmitField('Search')