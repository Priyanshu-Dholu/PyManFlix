from flask import Flask, render_template, request, redirect
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

# Delete Movie Function
@app.route('/delete/<int:id>')
def delete(id):
    movie = Movies.query.filter_by(id=id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect(location='/')

# Delete Movie Page
@app.route('/delete_movie')
def delete_movie():
    all_movies = Movies.query.all()
    return render_template('delete_movie.html',all_movies=all_movies)
    
# Update Movie Function
@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    movie = Movies.query.filter_by(id=id).first()
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.year = request.form['year']
        movie.link = request.form['link']
        db.session.commit()
        return redirect(location='/')
    
    return render_template('update_movie.html',movie=movie)


if __name__ == '__main__':
    app.run(debug=True)