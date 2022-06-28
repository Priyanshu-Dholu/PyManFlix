from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import login_user, current_user, logout_user, login_required
from manflix import app, db, bcrypt
from manflix.functions import get_movie_detail, get_movie_id
from manflix.forms import AddMovieForm, SearchMovieForm, RegistrationForm, LoginForm
from manflix.models import Movies, UserData


#------------------- All Pages ---------------------

# Index Page
@app.route('/')
def index():
    all_movies = Movies.query.order_by(Movies.id.desc()).limit(3)
    return render_template('index.html',all_movies=all_movies)

# Login
@app.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()   
    if form.is_submitted():        
        user = UserData.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):            
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'You Are Logged In!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Please Check For Username and Password', 'danger')        
    return render_template('login.html',title='Login',form=form)

# Log Out
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# Home Page
@app.route('/home')
@login_required
def home():
    page = request.args.get('page',1,type = int)
    all_movies = Movies.query.order_by(Movies.id.desc()).paginate(per_page = 3)
    curr_page = 'home'
    return render_template('home.html', all_movies=all_movies,current=curr_page)

# Add Movie Page
@app.route('/add_movies', methods=['GET', 'POST'])
@login_required
def add_movies():
    curr_page = 'add_movies'
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
            return render_template('add_movies.html', form1=form1,current=curr_page)   
        else:
            search = request.form["searched"]    
            movie_id = get_movie_id(search)    
            if movie_id:
                return render_template('add_movies.html', movie_id=movie_id, search=search,form1=form1,current=curr_page)
            else:
                flash(f'{ search } - Not Found!', 'danger')
                return render_template('add_movies.html', form1=form1,current=curr_page)                  
    return render_template('add_movies.html', form1=form1,current=curr_page)

# Movie Database Page
@app.route('/movie_database')
@login_required
def movie_database():
    curr_page = 'movie_database'
    all_movies = Movies.query.all()
    return render_template('movie_database.html', all_movies=all_movies,current=curr_page)

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

# User Registration Form
@app.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')       
        user = UserData(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account Has Been Created! You Can Now Log In', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

# Movie Screen
@app.route('/movie_screen/<int:id>')
@login_required
def movie_screen(id):
    movie = Movies.query.filter_by(id=id).first()
    link = movie.link[:-4] + 'raw=1'
    return render_template('movie_screen.html', movie=movie,link=link)


#------------------- All Functions ---------------------

# Delete Movie Function
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    movie = Movies.query.filter_by(id=id).first()
    db.session.delete(movie)
    db.session.commit()
    return render_template('movie_database.html')

# Update Movie Function
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
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


#------------------- All Error Pages ---------------------

# Error 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Error 500
@app.errorhandler(500)
def not_found(error):
    return render_template('500.html'),404