from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, Movie, User, Watchlist  
from werkzeug.utils import secure_filename
import os
from forms import LoginForm, RegisterForm, ReviewForm, AddMovieForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imdb_clone.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)

from models import User, Movie, Review
from forms import LoginForm, RegisterForm, ReviewForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_test_data():
    with app.app_context():
        db.create_all()

        
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', email='admin@example.com', password=generate_password_hash('admin'), is_admin=True)
            db.session.add(admin_user)

        if not User.query.filter_by(username='user1').first():
            user1 = User(username='user1', email='user1@example.com', password=generate_password_hash('password'))
            db.session.add(user1)

        if not Movie.query.filter_by(title='Movie 1').first():
            movie1 = Movie(title='Movie 1', description='Description for Movie 1', release_year=2020, imdb_rating=7.5, poster_url='/static/images/movie1.jpg', genre='Action', release_date='2020-01-01')
            db.session.add(movie1)

        db.session.commit()


login_manager.login_view = 'login'
@app.route('/')
def index():
    genres = db.session.query(Movie.genre).distinct().all()
    release_years = db.session.query(Movie.release_year).distinct().all()

    
    genres = [g[0] for g in genres if g[0]]
    release_years = [y[0] for y in release_years if y[0]]

    return render_template('index.html', genres=genres, release_years=release_years)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    print(f"Request method: {request.method}")
    print(f"Form data: {request.form}")

    if form.validate_on_submit():
        print("Form validation passed!")
        user = User.query.filter_by(email=form.email.data).first()
        print(f"User found: {user}") 
        
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful')
            return redirect(url_for('index'))
        else:
            print("Invalid credentials!")
            flash('Invalid email or password')

    else:
        print("Form validation failed!")
        print(form.errors)  

    return render_template('login.html', form=form)



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    print(f"Request method: {request.method}")
    print(f"Form data: {request.form}")

    if form.validate_on_submit():
        print("Form validation passed!")
        
    
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            print("User already exists!")
            flash("Email is already registered. Please log in.")
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Error during registration: {e}")
            flash('An error occurred. Please try again.')

    else:
        print("Form validation failed!")
        print(form.errors) 

    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = ReviewForm()
    if form.validate_on_submit():
        try:
            print(f"User {current_user.username} is submitting a review with rating {form.rating.data}.")
            review = Review(
                content=form.content.data,
                rating=form.rating.data,
                user_id=current_user.id,
                movie_id=movie.id
            )
            db.session.add(review)
            db.session.commit()
            flash('Your review has been added')
            return redirect(url_for('index'))
        except Exception as e:
            print(f"Error submitting review: {e}")
            db.session.rollback()
            flash('An error occurred while submitting your review.')
    reviews = Review.query.filter_by(movie_id=movie.id).all()
    return render_template('movie_detail.html', movie=movie, form=form, reviews=reviews)

@app.route('/api/movies')
def get_movies():
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 6, type=int)
    search = request.args.get('search', '', type=str)
    genre = request.args.get('genre', '', type=str)
    release_year = request.args.get('release_year', '', type=int)
    order_by = request.args.get('orderBy', 'title', type=str)  
    order = request.args.get('order', 'asc', type=str)

    query = Movie.query.order_by(getattr(getattr(Movie, order_by), order)()) if hasattr(Movie, order_by) else Movie.query
    if search:
        query = query.filter(Movie.title.ilike(f'%{search}%'))
    if genre:
        query = query.filter(Movie.genre.ilike(f'%{genre}%'))
    if release_year !=0:
        query = query.filter(Movie.release_year == release_year)

    movies = query.offset(offset).limit(limit).all()
    total = Movie.query.count()
    return jsonify([{
        'id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        'imdb_rating': movie.imdb_rating,
        'poster_url': movie.poster_url,
        'genre': movie.genre,
        'description': movie.description
    } for movie in movies]), {'X-Total-Count': total}



app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        file = form.poster.data
        filename = 'default.jpg'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        new_movie = Movie(
            title=form.title.data,
            description=form.description.data,
            release_year=form.release_year.data,
            genre=form.genre.data,
            imdb_rating=0.0, 
            poster_url='',  
            release_date=''  
        )
        db.session.add(new_movie)
        db.session.commit()
        flash('Movie added successfully')
        return redirect(url_for('index'))

    return render_template('add_movie.html', form=form, errors=form.errors)

@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = AddMovieForm(obj=movie)
    if form.validate_on_submit():
        file = form.poster.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            movie.poster_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        movie.title = form.title.data
        movie.description = form.description.data
        movie.release_year = form.release_year.data
        movie.genre = form.genre.data
        db.session.commit()
        flash('Movie updated successfully')
        return redirect(url_for('index'))
    return render_template('edit_movie.html', form=form, movie=movie, errors=form.errors)

@app.route('/delete_movie/<int:movie_id>')
@login_required
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully')
    return redirect(url_for('index'))





@app.route('/watchlist')
@login_required
def watchlist():
    watchlist_movies = Movie.query.join(Watchlist).filter(Watchlist.user_id == current_user.id).all()
    return render_template('watchlist.html', movies=watchlist_movies)

@app.route('/my_ratings')
@login_required
def my_ratings():
    user_reviews = Review.query.filter_by(user_id=current_user.id).all()
    return render_template('my_ratings.html', reviews=user_reviews)

@app.route('/add_to_watchlist/<int:movie_id>')
@login_required
def add_to_watchlist(movie_id):
    if not Watchlist.query.filter_by(user_id=current_user.id, movie_id=movie_id).first():
        new_entry = Watchlist(user_id=current_user.id, movie_id=movie_id)
        db.session.add(new_entry)
        db.session.commit()
        flash('Movie added to your watchlist.')
    else:
        flash('Movie is already in your watchlist.')
    return redirect(url_for('movie_detail', movie_id=movie_id))


if __name__ == '__main__':
    create_test_data()  
    app.run(debug=True)