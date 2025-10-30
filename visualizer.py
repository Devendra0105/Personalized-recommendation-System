import matplotlib.pyplot as plt

def create_analysis_report(movies, ratings, movie_stats):
    print("Generating analysis report...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Movie Dataset Analysis Report', fontsize=16, fontweight='bold')
    
    rating_counts = ratings['rating'].value_counts().sort_index()
    axes[0,0].bar(rating_counts.index, rating_counts.values, color='steelblue', alpha=0.7)
    axes[0,0].set_title('Distribution of Movie Ratings')
    axes[0,0].set_xlabel('Rating')
    axes[0,0].set_ylabel('Number of Ratings')
    for i, v in enumerate(rating_counts.values):
        axes[0,0].text(rating_counts.index[i], v + 50, str(v), ha='center', fontsize=9)
    
    genre_counts = {}
    for genre_list in movies['genres']:
        for genre in genre_list.split('|'):
            if genre != '(no genres listed)':
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    top_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    genres, counts = zip(*top_genres)
    
    axes[0,1].barh(genres, counts, color='darkorange', alpha=0.7)
    axes[0,1].set_title('Top 10 Genres by Movie Count')
    axes[0,1].set_xlabel('Number of Movies')
    
    user_activity = ratings.groupby('userId')['rating'].count()
    axes[1,0].hist(user_activity, bins=30, color='green', alpha=0.7, edgecolor='black')
    axes[1,0].set_title('Distribution of User Activity')
    axes[1,0].set_xlabel('Ratings per User')
    axes[1,0].set_ylabel('Number of Users')
    axes[1,0].axvline(user_activity.mean(), color='red', linestyle='--', 
                     label=f'Mean: {user_activity.mean():.1f}')
    axes[1,0].legend()
    
    high_rated = movie_stats[movie_stats['rating_count'] >= 50].nlargest(8, 'avg_rating')
    movie_titles = []
    for movie_id in high_rated['movieId']:
        title = movies[movies['movieId'] == movie_id]['title'].values[0]
        movie_titles.append(title[:30] + '...' if len(title) > 30 else title)
    
    axes[1,1].barh(movie_titles, high_rated['avg_rating'], color='purple', alpha=0.7)
    axes[1,1].set_title('Highest Rated Movies (min 50 reviews)')
    axes[1,1].set_xlabel('Average Rating')
    
    plt.tight_layout()
    plt.savefig('movie_analysis_report.png', dpi=100, bbox_inches='tight')
    plt.show()

def create_recommendation_chart(top_movies, display_name):
    movie_titles = []
    for title in top_movies['title']:
        if len(title) > 35:
            movie_titles.append(title[:35] + '...')
        else:
            movie_titles.append(title)
    
    plt.figure(figsize=(12, 6))
    
    y_pos = range(len(top_movies))
    bars = plt.barh(y_pos, top_movies['avg_rating'], color='teal', alpha=0.7)
    
    plt.yticks(y_pos, movie_titles)
    plt.xlabel('Average Rating')
    plt.title(f'Top {display_name} Movies by Rating and Popularity')
    plt.gca().invert_yaxis()
    
    for i, (bar, rating, count) in enumerate(zip(bars, top_movies['avg_rating'], top_movies['rating_count'])):
        plt.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, 
                f'{rating:.2f} ({int(count)} reviews)', 
                ha='left', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{display_name}_recommendations.png', dpi=100, bbox_inches='tight')
    plt.show()

def print_dataset_summary(movies, ratings):
    print("DATASET SUMMARY")
    print("=" * 50)
    
    avg_rating = ratings['rating'].mean()
    total_users = ratings['userId'].nunique()
    total_movies_with_ratings = ratings['movieId'].nunique()
    
    print(f"Basic Statistics:")
    print(f"  Total movies: {len(movies)}")
    print(f"  Total ratings: {len(ratings)}")
    print(f"  Unique users: {total_users}")
    print(f"  Rated movies: {total_movies_with_ratings}")
    print(f"  Average rating: {avg_rating:.2f}/5")
    
    print(f"Rating Distribution:")
    rating_dist = ratings['rating'].value_counts().sort_index()
    for rating, count in rating_dist.items():
        percentage = (count / len(ratings)) * 100
        print(f"  {rating}/5: {count:>6} ratings ({percentage:4.1f}%)")
    
    genre_counts = {}
    for genre_list in movies['genres']:
        for genre in genre_list.split('|'):
            if genre != '(no genres listed)':
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    print(f"Genre Information:")
    print(f"  Total genres: {len(genre_counts)}")
    print(f"  Top 5 genres:")
    for genre, count in sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"    {genre}: {count} movies")