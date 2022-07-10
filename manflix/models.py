from manflix import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return UserData.query.get(int(user_id))

# Movie Database
class Movies(db.Model):
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

# User Database
class UserData(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    email = db.Column(db.String(120),nullable=False)  
    avatar =  db.Column(db.String(15),nullable=False)
    otp = db.Column(db.String(4))
    is_verified = db.Column(db.Boolean,default=False)
    is_admin = db.Column(db.Boolean,default=False)
    
    def __refr__(self):
        return f"User('{self.username}','{self.is_admin}','{self.email}','{self.is_verified}','{self.otp}','{self.user_image}')"