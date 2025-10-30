import pandas as pd

def load_movie_data():
    movies = pd.read_csv('ml-latest-small/movies.csv')
    ratings = pd.read_csv('ml-latest-small/ratings.csv')
    return movies, ratings

def prepare_movie_stats(movies, ratings):
    movie_stats = ratings.groupby('movieId').agg({
        'rating': ['count', 'mean']
    }).round(3)
    movie_stats.columns = ['rating_count', 'avg_rating']
    movie_stats = movie_stats.reset_index()
    
    movies_with_stats = movies.merge(movie_stats, on='movieId')
    return movies_with_stats

def get_all_genres(movies):
    all_genres = set()
    for genre_list in movies['genres']:
        genres = genre_list.split('|')
        all_genres.update(genres)
    
    all_genres.discard('(no genres listed)')
    return sorted(list(all_genres))