import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def collaborative_filtering(user_id, ratings, movies, n_recommendations=10):
    """Simple collaborative filtering based on user similarity"""
    print(f"Collaborative recommendations for user {user_id}")
    
    # Create user-item matrix
    user_item_matrix = ratings.pivot_table(
        index='userId', 
        columns='movieId', 
        values='rating'
    ).fillna(0)
    
    if user_id not in user_item_matrix.index:
        print("User not found in rating matrix")
        return []
    
    # Calculate user similarity
    user_similarity = cosine_similarity(user_item_matrix)
    user_sim_df = pd.DataFrame(
        user_similarity, 
        index=user_item_matrix.index, 
        columns=user_item_matrix.index
    )
    
    # Get similar users
    similar_users = user_sim_df[user_id].sort_values(ascending=False)[1:6]
    
    # Get movies liked by similar users
    user_rated = set(ratings[ratings['userId'] == user_id]['movieId'])
    recommendations = {}
    
    for sim_user_id, similarity in similar_users.items():
        sim_user_ratings = ratings[ratings['userId'] == sim_user_id]
        high_rated = sim_user_ratings[sim_user_ratings['rating'] >= 4.0]
        
        for _, rating in high_rated.iterrows():
            if rating['movieId'] not in user_rated:
                if rating['movieId'] not in recommendations:
                    recommendations[rating['movieId']] = []
                recommendations[rating['movieId']].append(similarity * rating['rating'])
    
    # Calculate average scores
    movie_scores = {}
    for movie_id, scores in recommendations.items():
        movie_scores[movie_id] = np.mean(scores)
    
    # Get top recommendations
    top_recommendations = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:n_recommendations]
    
    return top_recommendations

def hybrid_recommendations(user_id, genre_input, movies_with_stats, ratings, all_genres, num_movies=10):
    """Combine content-based and collaborative filtering"""
    from recommender import get_genre_recommendations
    
    # Get content-based recommendations
    content_movies, display_name = get_genre_recommendations(genre_input, movies_with_stats, all_genres, num_movies * 2)
    
    # Get collaborative recommendations
    collab_recs = collaborative_filtering(user_id, ratings, movies_with_stats, num_movies)
    
    print(f"Hybrid recommendations for {display_name}")
    print("Combining content-based and collaborative approaches...")
    
    # Simple hybrid: take top from both
    hybrid_results = []
    
    if content_movies is not None:
        for i, (_, movie) in enumerate(content_movies.head(num_movies//2).iterrows(), 1):
            print(f"{i}. {movie['title']} (Content-based)")
            hybrid_results.append(movie)
    
    if collab_recs:
        for i, (movie_id, score) in enumerate(collab_recs[:num_movies//2], len(hybrid_results) + 1):
            movie_title = movies_with_stats[movies_with_stats['movieId'] == movie_id]['title'].values[0]
            print(f"{i}. {movie_title} (Collaborative)")
    
    return hybrid_results