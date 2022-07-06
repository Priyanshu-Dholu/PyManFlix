from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
from werkzeug.utils import secure_filename
import random,smtplib,secrets,os
from manflix import app, db, bcrypt
from manflix.functions import get_movie_detail, get_movie_id
from manflix.forms import AddMovieForm, SearchMovieForm, RegistrationForm, LoginForm, VerifyUserForm, AdminForm, UpdateAccountForm
from manflix.models import Movies, UserData

#------------------- All Pages ---------------------
# Index Page
@app.route('/')
def index():
    try:
        all_movies = Movies.query.order_by(Movies.id.desc()).limit(3)
        print(all_movies)        
        return render_template('index.html',all_movies=all_movies)
    except:
        return render_template('index.html')

# Login
@app.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()   
    if form.is_submitted():        
        user = UserData.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.is_verified == True:            
            login_user(user,remember=form.remember.data)
            session["email"] = user.email
            next_page = request.args.get('next')
            flash(f'You Are Logged In!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))        
        else:
            flash(f'Please Check For Username and Password', 'danger')        
    return render_template('login.html',title='Login',form=form)

# User Registration Form
@app.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user_name = form.username.data  
        e_mail = form.email.data   
        otp = ''.join([str(random.randint(0, 9)) for i in range(4)])
        user_avatar = form.user_avatar.data + '.jpg'
        print(user_avatar)
        print(type(user_avatar))        
        user = UserData(username=user_name,email=e_mail,password=hashed_password,otp=otp,user_image=user_avatar)

        # Adding Current Users Email To Session
        session["email"] = form.email.data

        # Sending OTP To Mail 
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login('johnharrison12587@gmail.com', 'fhwrnydeedhztaso')
        message = 'Subject: {}\n\n{}'.format('Verification Code For ' + str(user_name), 'Your Verification Code is: ' + str(otp)) 
        smtp_server.sendmail('johnharrison12587@gmail.com', form.email.data, message)
        smtp_server.quit()  
        
        # Commiting Changes
        db.session.add(user)
        db.session.commit()
        flash(f'Please Verify Your Account!', 'info')                
        return redirect(url_for('verify'))
    return render_template('register.html',form=form)

# User Verify Page
@app.route('/verify',methods=['GET','POST'])
def verify():
    form2 = VerifyUserForm() 
    if "email" in session:
            email = session["email"]
            check_user = UserData.query.filter_by(email=email).first()    
            user_otp = form2.otp.data              
            if form2.validate_on_submit():                        
                if user_otp == check_user.otp:                      
                    check_user.is_verified = True
                    db.session.commit()
                    flash(f'You Can Log In Now!', 'success') 
                    return redirect(url_for('login'))
                elif user_otp != check_user.otp:
                    flash(f'Wrong OTP Account Deleted From DB!', 'danger')                
                    db.session.delete(check_user)                
                    db.session.commit()
                    return render_template('index.html')
            return render_template('verify.html',form2=form2)
    return redirect(url_for('register'))

# Become Admin Page
@app.route('/become_admin',methods=['GET','POST'])
@login_required
def become_admin():
    form = AdminForm()    
    if form.is_submitted():
        check_user = UserData.query.filter_by(email=form.email.data).first()    
        check_user.is_admin = True
        db.session.commit()
        flash('You Are Admin Now','success')
        return redirect(url_for('home'))
    
    return render_template('become_admin.html',form=form)


@app.route('/account',methods=['GET','POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='Profile_Icon/' + current_user.user_image)
    return render_template('account.html',title='Account',image_file=image_file,form=form)

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
    
    return render_template('home.html', all_movies=all_movies)

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
@login_required
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