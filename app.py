from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, Movie, User, Watchlist  
from forms import LoginForm, RegisterForm, ReviewForm, AddMovieForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///imdb_clone.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Movie, Review
from forms import LoginForm, RegisterForm, ReviewForm

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    with app.app_context():
        db.create_all()

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

@app.route('/movie/<int:movie_id>/review', methods=['GET', 'POST'])
@login_required
def review(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            content=form.content.data,
            rating=form.rating.data,
            user_id=current_user.id,
            movie_id=movie.id
        )
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added')
        return redirect(url_for('movie_detail', movie_id=movie.id))
    return render_template('review.html', form=form, movie=movie)

@app.route('/api/movies')
def get_movies():
    offset = request.args.get('offset', 0, type=int)
    limit = request.args.get('limit', 6, type=int)
    search = request.args.get('search', '', type=str)
    genre = request.args.get('genre', '', type=str)
    release_year = request.args.get('release_year', '', type=str)

    query = Movie.query

    if search:
        query = query.filter(Movie.title.ilike(f'%{search}%'))
    if genre:
        query = query.filter(Movie.genre.ilike(f'%{genre}%'))
    if release_year:
        query = query.filter(Movie.release_year == int(release_year))

    movies = query.offset(offset).limit(limit).all()
    return jsonify([{
        'id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        'imdb_rating': movie.imdb_rating,
        'poster_url': movie.poster_url
    } for movie in movies])

@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    if not current_user.is_admin:
        flash('You do not have permission to access this page.')
        return redirect(url_for('index'))

    form = AddMovieForm()
    if form.validate_on_submit():
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
        flash('Movie added successfully!')
        return redirect(url_for('index'))

    return render_template('add_movie.html', form=form)

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
    with app.app_context():
        db.create_all()
    app.run(debug=True) 