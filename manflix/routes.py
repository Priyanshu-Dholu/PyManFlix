from flask import Flask, render_template, request, redirect, flash, url_for
from tmdbv3api import TMDb, Movie
from manflix import app, db
from manflix.forms import AddMovieForm, SearchMovieForm
from manflix.models import Movies
from manflix import db

# Error Page 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Error Page 500
@app.errorhandler(500)
def not_found(error):
    return render_template('500.html'),404

# Home Page
@app.route('/')
def home():
    all_movies = Movies.query.all()
    return render_template('index.html', all_movies=all_movies)

# Searh Movie Page In Database
@app.route('/search_movies', methods=['POST'])
def search_movies():
    if request.method == 'POST':              
        tag = request.form["searched"]
        search = "%{}%".format(tag)        
        mov = Movies.query.filter(Movies.title.like(search)).all()
        
        if mov:
            return render_template('search_movies.html', mov=mov,search=tag)
        else:
            movie_from_db = Movies.query.all()
            return render_template('search_movies.html', mov=mov,search=tag)

# Add Movie Page
@app.route('/add_movies', methods=['GET', 'POST'])
def add_movies():
    form1 = AddMovieForm()    
    if request.method == 'POST':
        if form1.validate_on_submit():
            link = form1.link.data
            quality = form1.quality.data
            movie_id_tmd = form1.movie_id_tmd.data
            dolby_audio = form1.dolby_audio.data
            dual_audio = form1.dual_audio.data
            poster_link = get_movie_detail(1, movie_id_tmd)
            title = get_movie_detail(2, movie_id_tmd)            
            movie_release_year = get_movie_detail(3, movie_id_tmd)
            movie_backdrop_link = get_movie_detail(4, movie_id_tmd)            
            trailer_link = get_movie_detail(6, movie_id_tmd)
            movie = Movies(title=title, link=link, quality=quality,movie_release_year=movie_release_year, movie_id_tmd=movie_id_tmd, poster_link=poster_link, movie_backdrop_link=movie_backdrop_link,trailer_link=trailer_link, dolby_audio=dolby_audio, dual_audio=dual_audio)
            db.session.add(movie)
            db.session.commit()
            flash(f'{ title } - Added Successfully!', 'success')
            return render_template('add_movies.html', form1=form1)   
        else:
            search = request.form["searched"]    
            movie_id = get_movie_id(search)    
            if movie_id:
                return render_template('add_movies.html', movie_id=movie_id, search=search,form1=form1)
            else:
                flash(f'{ search } - Not Found!', 'danger')
                return render_template('add_movies.html', form1=form1)                  
    return render_template('add_movies.html', form1=form1)

# Movie Database Page
@app.route('/movie_database')
def movie_database():
    all_movies = Movies.query.all()
    return render_template('movie_database.html', all_movies=all_movies)

# Delete Movie Function
@app.route('/delete/<int:id>')
def delete(id):
    movie = Movies.query.filter_by(id=id).first()
    db.session.delete(movie)
    db.session.commit()
    return url_for(movie_database)


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
    link = movie.link[:-4] + 'raw=1'
    return render_template('movie_screen.html', movie=movie,link=link)


# TMDB API Section
tmdb = TMDb()
tmdb.api_key = 'fb86432acfe5114ca73b86d4cbe66ef2'
tmdb.language = 'en'
tmdb.debug = True

# Function To Get Movie Details
def get_movie_detail(operation, movie_id_tmd):    
    movie = Movie()
    m = movie.details(movie_id_tmd)
    if operation == 1:
        link = f'https://image.tmdb.org/t/p/w220_and_h330_face/{m.poster_path}'
        return link
    elif operation == 2:
        return f'{m.original_title}'
    elif operation == 3:
        return int(m.release_date[:4])
    elif operation == 4:
        return f'https://image.tmdb.org/t/p/w1280{m.backdrop_path}'
    elif operation == 5:
        return f'{m.overview}'
    elif operation == 6:
        link = m['videos']['results'][0]["key"]           
        return 'https://www.youtube.com/embed/' + link
    else:
        return 'Error'

# Function To Get Movie ID
def get_movie_id(movie_name):
    movie = Movie()
    search = movie.search(movie_name)
    movie_list_id = []      
    movie_list_title = []
    movie_list_poster = []
    final = []
    for i in search:
        for z in i:
            if z == 'id':
                movie_list_id.append(i[z])
            elif z == 'title':
                movie_list_title.append(i[z])                
            elif z == 'poster_path':
                movie_list_poster.append(i[z])     
            final = list(zip(movie_list_id,movie_list_title , movie_list_poster))                       
    
    return final
