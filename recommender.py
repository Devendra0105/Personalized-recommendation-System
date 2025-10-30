import numpy as np

def get_genre_recommendations(genre_input, movies_with_stats, all_genres, num_movies=10):
    if '+' in genre_input:
        genres = [g.strip() for g in genre_input.split('+')]
        display_name = ' + '.join(genres)
    else:
        genres = [genre_input.strip()]
        display_name = genre_input
    
    invalid_genres = [g for g in genres if g not in all_genres]
    if invalid_genres:
        print(f"Unknown genres: {', '.join(invalid_genres)}")
        return None, None
    
    print(f"Finding {num_movies} {display_name} movies...")
    
    genre_movies = movies_with_stats.copy()
    for genre in genres:
        genre_movies = genre_movies[genre_movies['genres'].str.contains(genre)]
    
    if len(genre_movies) == 0:
        print(f"No movies found for {display_name}")
        return None, None
    
    reliable_movies = genre_movies[genre_movies['rating_count'] >= 10]
    
    if len(reliable_movies) == 0:
        print(f"No popular movies found for {display_name}")
        return None, None
    
    reliable_movies = reliable_movies.copy()
    reliable_movies['score'] = (
        reliable_movies['avg_rating'] * 
        np.log1p(reliable_movies['rating_count'])
    )
    
    top_movies = reliable_movies.sort_values('score', ascending=False).head(num_movies)
    
    return top_movies, display_name

def print_recommendations(top_movies, display_name):
    if top_movies is None:
        return
    
    print(f"Top {len(top_movies)} {display_name} movies:")
    print("-" * 60)
    
    for i, (_, movie) in enumerate(top_movies.iterrows(), 1):
        print(f"{i:2d}. {movie['title']}")
        print(f"    Rating: {movie['avg_rating']}/5 from {int(movie['rating_count'])} reviews")
        print(f"    Genres: {movie['genres'].replace('|', ', ')}")
        print()