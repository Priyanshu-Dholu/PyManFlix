from datetime import datetime
from manflix import db

# Movie Database
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True)    
    link = db.Column(db.String(500))
    quality = db.Column(db.Boolean)
    movie_id_tmd = db.Column(db.Integer)
    movie_release_year = db.Column(db.Integer)
    poster_link = db.Column(db.String(500))
    movie_backdrop_link = db.Column(db.String(500))    
    trailer_link = db.Column(db.String(125))
    dolby_audio = db.Column(db.Boolean)
    dual_audio = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f"movies('{self.title}','{self.link}',{self.quality}',{self.movie_release_year},'{self.dolby_audio}','{self.dual_audio},{self.poster_link},{self.movie_id_tmd}','{self.movie_backdrop_link}','{self.trailer_link}')"