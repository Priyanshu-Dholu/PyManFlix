from datetime import datetime
from manflix import db

# Movie Database
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.varchar(80), unique=True)
    year = db.Column(db.Integer)
    link = db.Column(db.varchar(500))
    quality = db.Column(db.boolean)
    movie_id_tmd = db.Column(db.Integer)
    poster_link = db.Column(db.varchar(500))
    movie_backdrop_link = db.Column(db.varchar(500))
    movie_overview = db.Column(db.varchar(500))
    trailer_link = db.Column(db.varchar(125))
    dolby_audio = db.Column(db.boolean)
    dual_audio = db.Column(db.boolean)

    def __repr__(self) -> str:
        return f"movies('{self.title}','{self.year}','{self.link}',{self.quality}','{self.dolby_audio}','{self.dual_audio},{self.poster_link},{self.movie_id_tmd}','{self.movie_backdrop_link}','{self.movie_overview}','{self.trailer_link}')"