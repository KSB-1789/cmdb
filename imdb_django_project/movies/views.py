from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Movie, Review, Watchlist 
from .forms import ReviewForm, MovieForm
from profiles.forms import RegisterForm
from django.db.models import Q

def index(request):
    movies = Movie.objects.all().order_by('title')
    # Filters
    search_query = request.GET.get('search', '')
    genre_query = request.GET.get('genre', '')
    release_year_query = request.GET.get('release_year', '')

    if search_query:
        movies = movies.filter(Q(title__icontains=search_query))
    if genre_query:
        movies = movies.filter(genre__icontains=genre_query)
    if release_year_query:
        movies = movies.filter(release_year=release_year_query)

    # Pagination
    paginator = Paginator(movies, 8)
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)

    # Genres and years
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    release_years = Movie.objects.values_list('release_year', flat=True).distinct().order_by('release_year')

    context = {
        'movies': movies,
        'genres': genres,
        'release_years': release_years,
    }
    return render(request, 'movies/index.html', context)


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie).order_by('-created_at')
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movies:movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()

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
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('movies:index')


@login_required
def my_ratings(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    context = {'reviews': reviews}
    return render(request, 'movies/my_ratings.html', context)


@login_required
def watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    movies = [item.movie for item in watchlist_items]
    context = {'movies': movies}
    return render(request, 'movies/watchlist.html', context)