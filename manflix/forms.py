from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField, RadioField
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
    user_avatar = RadioField('Choose Avatar', validators=[DataRequired()],choices=[('1','Iron Man'),('2','Spider Man'),('3','Hulk'),('4','Groot'),('5','Scarlet Witch'),('6','Vision'),('7','Ant Man'),('8','Wasp'),('9','Natasha'),('10','Black Panther')])                                     
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

# Update User Form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email = EmailField('Email',validators=[DataRequired(),Email()])    
    picture = FileField('Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    user_avatar = RadioField('Choose Avatar', choices=[('1','Iron Man'),('2','Spider Man'),('3','Hulk'),('4','Groot'),('5','Scarlet Witch'),('6','Vision'),('7','Ant Man'),('8','Scarlet Witch'),('9','Natasha'),('10','Black Panther')])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = UserData.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username Is Already Taken. Please Use Another Username!')
    def validate_email(self,email):
        if email.data != current_user.email:
            user = UserData.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is Already Registered. Log In!')

# Verify User Form
class VerifyUserForm(FlaskForm):
    otp = StringField('OTP', validators=[DataRequired()])
    submit = SubmitField('Verify')    

# Become Admin Form
class AdminForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Become Admin')

# Form Class For Searching Movie
class SearchMovieForm(FlaskForm):
    movie_name = StringField('Search For Movie Movie ID', validators=[DataRequired()])
    submit = SubmitField('Search')