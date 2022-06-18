from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tmdbv3api import TMDb, Movie

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
    quality = db.Column(db.Boolean)
    movie_id_tmd = db.Column(db.Integer)
    poster_link = db.Column(db.String(500))
    movie_backdrop_link = db.Column(db.String(500))
    movie_overview = db.Column(db.String(500))
    dolby_audio = db.Column(db.Boolean)
    dual_audio = db.Column(db.Boolean)
    added_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"movies('{self.title}','{self.year}','{self.link}','{self.added_on},{self.quality}','{self.dolby_audio}','{self.dual_audio},{self.poster_link},{self.movie_id_tmd}','{self.movie_backdrop_link}','{self.movie_overview}')"

# Home Page


@app.route('/home')
def home():
    all_movies = Movies.query.all()

    return render_template('index.html', all_movies=all_movies)

# Add Movie Page


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        link = request.form['link']
        quality = request.form.get('quality')
        movie_id_tmd = request.form['movie_id_tmd']
        title = get_movie_detail(2, movie_id_tmd)
        year = get_movie_detail(3, movie_id_tmd)
        poster_link = get_movie_detail(1, movie_id_tmd)
        movie_backdrop_link = get_movie_detail(4, movie_id_tmd)
        movie_overview = get_movie_detail(5, movie_id_tmd)
        if quality == None:
            quality = False
        else:
            quality = True

        dolby_audio = request.form.get('dolby_audio')

        if dolby_audio == None:
            dolby_audio = False
        else:
            dolby_audio = True
        dual_audio = request.form.get('dual_audio')
        if dual_audio == None:
            dual_audio = False
        else:
            dual_audio = True
        movies = Movies(title=title, year=year, link=link, quality=quality,
                        dolby_audio=dolby_audio, dual_audio=dual_audio, poster_link=poster_link, movie_id_tmd=movie_id_tmd, movie_backdrop_link=movie_backdrop_link,movie_overview=movie_overview)
        db.session.add(movies)
        db.session.commit()

    all_movies = Movies.query.all()
    print(all_movies)
    return render_template('add_movies.html', all_movies=all_movies)

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
    return render_template('delete_movie.html', all_movies=all_movies)

# Update Movie Function


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    movie = Movies.query.filter_by(id=id).first()
    if request.method == 'POST':
        movie.title = request.form['title']
        movie.year = request.form['year']
        movie.link = request.form['link']
        quality = request.form.get('quality')
        if quality == False:
            quality = True
        elif quality == True:
            quality = False
        db.session.commit()
        return redirect(location='/')

    return render_template('update_movie.html', movie=movie)

# Movie Screen


@app.route('/movie_screen/<int:id>')
def movie_screen(id):
    movie = Movies.query.filter_by(id=id).first()
    return render_template('movie_screen.html', movie=movie)


def get_movie_detail(operation, movie_id_tmd):
    tmdb = TMDb()
    tmdb.api_key = 'fb86432acfe5114ca73b86d4cbe66ef2'
    tmdb.language = 'en'
    tmdb.debug = True
    movie = Movie()
    m = movie.details(movie_id_tmd)
    if operation == 1:
        link = f'https://image.tmdb.org/t/p/w220_and_h330_face/{m.poster_path}'
        return link
    elif operation == 2:
        return f'{m.original_title}'
    elif operation == 3:
        return f'{m.release_date}'
    elif operation == 4:
        return f'https://image.tmdb.org/t/p/w1280{m.backdrop_path}'
    elif operation == 5:
        return f'{m.overview}'
    else:
        return 'Error'


if __name__ == '__main__':
    app.run(debug=True)
