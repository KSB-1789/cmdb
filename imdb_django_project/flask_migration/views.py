from django.shortcuts import render
from django.db.models import Q
from movies.models import Movie

def search_movies(request):
    query = request.GET.get('q', '')
    genre = request.GET.get('genre', '')
    
    movies = Movie.objects.all()
    
    if query:
        movies = movies.filter(
            Q(title__icontains=query) |
            Q(genre__icontains=query)
        )
    
    if genre:
        movies = movies.filter(genre=genre)
    
    genres = Movie.objects.values_list('genre', flat=True).distinct()
    
    context = {
        'movies': movies,
        'genres': genres,
        'query': query,
        'selected_genre': genre
    }
    return render(request, 'flask_migration/search.html', context) 