from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

# Form Class For Adding Movie
class AddMovieForm(FlaskForm):

    link = StringField('Link', validators=[DataRequired()])
    movie_id_tmd = StringField('TMDB Movie ID', validators=[DataRequired()])
    quality = BooleanField('Quality', default='checked')
    dolby_audio = BooleanField('Dolby Audio', default='checked')
    dual_audio = BooleanField('Dual Audio', default='checked')
    submit = SubmitField('Add Movie')

# Form Class For Searching Movie
class SearchMovieForm(FlaskForm):
    movie_name = StringField('Search For Movie Movie ID', validators=[DataRequired()])
    submit = SubmitField('Search')