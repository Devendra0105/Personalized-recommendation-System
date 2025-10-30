import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split

def evaluate_recommendation_accuracy(ratings, movies_with_stats):
    print("Evaluating Recommendation Accuracy")
    print("=" * 40)
    
    # Split data for evaluation
    train_data, test_data = train_test_split(ratings, test_size=0.2, random_state=42)
    
    # Baseline: predict average rating
    avg_rating = train_data['rating'].mean()
    baseline_pred = [avg_rating] * len(test_data)
    
    rmse_baseline = np.sqrt(mean_squared_error(test_data['rating'], baseline_pred))
    mae_baseline = mean_absolute_error(test_data['rating'], baseline_pred)
    
    print(f"Baseline (Average Rating):")
    print(f"  RMSE: {rmse_baseline:.3f}")
    print(f"  MAE: {mae_baseline:.3f}")
    
    # Simple user-average model
    user_avg = train_data.groupby('userId')['rating'].mean()
    user_pred = []
    
    for _, row in test_data.iterrows():
        user_id = row['userId']
        if user_id in user_avg.index:
            user_pred.append(user_avg[user_id])
        else:
            user_pred.append(avg_rating)
    
    rmse_user = np.sqrt(mean_squared_error(test_data['rating'], user_pred))
    mae_user = mean_absolute_error(test_data['rating'], user_pred)
    
    print(f"User-Average Model:")
    print(f"  RMSE: {rmse_user:.3f}")
    print(f"  MAE: {mae_user:.3f}")
    
    return {
        'baseline': {'rmse': rmse_baseline, 'mae': mae_baseline},
        'user_avg': {'rmse': rmse_user, 'mae': mae_user}
    }

def calculate_precision(top_movies, test_data, user_id=1, k=10):
    """Calculate Precision@K for recommendations"""
    if top_movies is None:
        return 0
    
    # Get user's highly rated movies from test set
    user_test_ratings = test_data[test_data['userId'] == user_id]
    user_high_rated = user_test_ratings[user_test_ratings['rating'] >= 4.0]
    
    if len(user_high_rated) == 0:
        return 0
    
    # Check how many recommended movies user actually liked
    recommended_ids = set(top_movies['movieId'].head(k))
    liked_ids = set(user_high_rated['movieId'])
    
    hits = len(recommended_ids.intersection(liked_ids))
    precision = hits / k
    
    print(f"Precision@{k}: {precision:.3f} ({hits}/{k} relevant)")
    return precision