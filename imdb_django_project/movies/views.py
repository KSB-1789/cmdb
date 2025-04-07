from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Movie, Review, Watchlist 
from .forms import ReviewForm, MovieForm
from profiles.forms import RegisterForm
from django.db.models import Q
from django.contrib import messages

def index(request):
    movies = Movie.objects.all().order_by('-rating')
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    
    search_query = request.GET.get('search', '')
    genre_query = request.GET.get('genre', '')
    
    if search_query:
        movies = movies.filter(Q(title__icontains=search_query))
    if genre_query:
        movies = movies.filter(genre=genre_query)
    
    context = {
        'movies': movies,
        'genres': genres,
        'search_query': search_query,
        'genre_query': genre_query,
    }
    return render(request, 'movies/index.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            messages.success(request, 'Your review has been added!')
            return redirect('movies:movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    
    # Get all reviews for this movie
    reviews = movie.reviews.all().order_by('-created_at')
    
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'movies/movie_detail.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('movies:login')
    else:
        form = RegisterForm()
    return render(request, 'movies/register.html', {'form': form})



class CustomLoginView(LoginView):
    template_name = 'movies/login.html'
    def get_success_url(self):
      return reverse('movies:index')


@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('movies:movie_detail', movie_id=movie.id)
    else:
        form = MovieForm()
    
    return render(request, 'movies/add_movie.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('movies:index')


@login_required
def my_ratings(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'movies/my_ratings.html', {'reviews': reviews})


@login_required
def watchlist(request):
    movies = Movie.objects.filter(watchlist_entries__user=request.user)
    return render(request, 'movies/watchlist.html', {'movies': movies})


@login_required
def ratings(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'reviews': reviews,
    }
    return render(request, 'movies/ratings.html', context)


def top_rated(request):
    movies = Movie.objects.all().order_by('-rating')[:25]
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'title': 'Top Rated Movies'
    })


def most_popular(request):
    movies = Movie.objects.all().order_by('-views')[:25]
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'title': 'Most Popular Movies'
    })


@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    watchlist_entry, created = Watchlist.objects.get_or_create(user=request.user, movie=movie)
    
    if not created:
        watchlist_entry.delete()
        messages.success(request, f'"{movie.title}" removed from your watchlist.')
    else:
        messages.success(request, f'"{movie.title}" added to your watchlist.')
    
    return redirect('movies:index')


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated!')
            return redirect('movies:my_ratings')
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'movies/edit_review.html', {
        'form': form,
        'review': review
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    movie_title = review.movie.title
    review.delete()
    messages.success(request, f'Your review for "{movie_title}" has been deleted.')
    return redirect('movies:my_ratings')

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id, added_by=request.user)
    movie_title = movie.title
    movie.delete()
    messages.success(request, f'"{movie_title}" has been deleted.')
    return redirect('movies:index')