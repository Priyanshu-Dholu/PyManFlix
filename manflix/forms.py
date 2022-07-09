from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, BooleanField, PasswordField, EmailField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from manflix.models import UserData

# Form Class For Adding Movie
class AddMovieForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    movie_id_tmd = StringField('TMDB Movie ID', validators=[DataRequired()])
    quality = BooleanField('Quality')
    dolby_audio = BooleanField('Dolby Audio')
    dual_audio = BooleanField('Dual Audio')
    submit = SubmitField('Add Movie')

# Form For Updating Movie
class UpdateMovieForm(FlaskForm):
    link = StringField('Link', validators=[DataRequired()])
    movie_id_tmd = StringField('TMDB Movie ID', validators=[DataRequired()])
    quality = BooleanField('Quality')
    dolby_audio = BooleanField('Dolby Audio')
    dual_audio = BooleanField('Dual Audio')
    submit = SubmitField('Update Movie')


# Registration Form For User
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min=2,max=20)])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])      
    user_avatar = SelectField('Select Avatar', choices=[('1', 'Iron Man'),
    ('2', 'Spider-Man'),
    ('3', 'Hulk'),
    ('4', 'Groot'),
    ('5', 'Ant-Man'),
    ('6', 'Wasp'),
    ('7', 'Black Panther'),
    ('8', 'Thanos'),
    ('9','Baymanx'),
    ('10', 'Phineas'),
    ('11', 'Perry'),
    ('12', 'Ferb'),
    ('13', 'Chuck'),
    ('14', 'Bolt'),
    ('15', 'Hiro'),
    ('16', 'Ralph'),
    ('17', 'Mickey'),    
    ])                             
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
    user_avatar = SelectField('Select Avatar', choices=[('1', 'Iron Man'),
    ('2', 'Spider-Man'),
    ('3', 'Hulk'),
    ('4', 'Groot'),
    ('5', 'Ant-Man'),
    ('6', 'Wasp'),
    ('7', 'Black Panther'),
    ('8', 'Thanos'),
    ('9','Baymax'),
    ('10', 'Phineas'),
    ('11', 'Perry'),
    ('12', 'Ferb'),
    ('13', 'Chuck'),
    ('14', 'Bolt'),
    ('15', 'Hiro'),
    ('16', 'Ralph'),
    ('17', 'Mickey'),    
    ])                             
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