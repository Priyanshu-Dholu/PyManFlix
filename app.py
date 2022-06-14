from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Movie Database
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    year = db.Column(db.Integer)    
    link = db.Column(db.String(500))
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"movies('{self.title}','{self.year}','{self.link}','{self.added_on}')"

# Home Page
@app.route('/home')
def home():
    all_movies = Movies.query.all()    
    return render_template('index.html',all_movies=all_movies)

# Add Movie Page
@app.route('/', methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        link = request.form['link']
        movies = Movies(title=title,year=year,link=link)
        db.session.add(movies)
        db.session.commit()

    all_movies = Movies.query.all()
    print(all_movies)    
    return render_template('add_movies.html',all_movies=all_movies)
    
    
# Just An Empty Page
@app.route('/show')
def show():
    all_movies = Movies.query.all()
    print(all_movies)
    return 'this is movie page'

if __name__ == '__main__':
    app.run(debug=True)