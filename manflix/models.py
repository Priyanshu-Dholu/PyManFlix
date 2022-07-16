from manflix import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return UserData.query.get(int(user_id))

# Movie Database
class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), unique=True)    
    link = db.Column(db.String(500))
    quality = db.Column(db.Boolean)
    movie_id_tmd = db.Column(db.Integer)
    category = db.Column(db.String(200))
    movie_release_year = db.Column(db.Integer)
    poster_link = db.Column(db.String(500))
    movie_backdrop_link = db.Column(db.String(500))    
    trailer_link = db.Column(db.String(125))
    dolby_audio = db.Column(db.Boolean)
    dual_audio = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f"movies('{self.title}','{self.category}','{self.link}',{self.quality}',{self.movie_release_year},'{self.dolby_audio}','{self.dual_audio},{self.poster_link},{self.movie_id_tmd}','{self.movie_backdrop_link}','{self.trailer_link}')"

class MovieLike(db.Model):
    __tablename__ = 'movie_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('userdata.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))

# User Database
class UserData(db.Model,UserMixin):
    __tablename__ = 'userdata'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    email = db.Column(db.String(120),nullable=False)  
    avatar =  db.Column(db.String(15),nullable=False)
    otp = db.Column(db.String(4))
    is_verified = db.Column(db.Boolean,default=False)
    is_admin = db.Column(db.Boolean,default=False)

    liked = db.relationship(
        'MovieLike',
        foreign_keys='MovieLike.user_id',
        backref='userdata', lazy='dynamic')

    def like_movie(self, movies):
        if not self.has_liked_movies(movies):
            like = MovieLike(user_id=self.id, movie_id=movies.id)
            db.session.add(like)

    def unlike_movies(self, movies):
        if self.has_liked_movies(movies):
            MovieLike.query.filter_by(
                user_id=self.id,
                movie_id=movies.id).delete()

    def has_liked_movies(self, movies):
        return MovieLike.query.filter(
            MovieLike.user_id == self.id,
            MovieLike.movie_id == movies.id).count() > 0
    
    def __refr__(self):
        return f"User('{self.username}','{self.is_admin}','{self.email}','{self.is_verified}','{self.otp}','{self.user_image}')"