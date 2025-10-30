
from data_loader import load_movie_data, prepare_movie_stats, get_all_genres
from recommender import get_genre_recommendations, print_recommendations
from visualizer import create_analysis_report, create_recommendation_chart, print_dataset_summary
from evaluator import evaluate_recommendation_accuracy, calculate_precision
from hybrid_recommeder import hybrid_recommendations

def show_genre_combinations():
    combinations = [
        "Comedy+Romance",
        "Action+Adventure", 
        "Sci-Fi+Fantasy",
        "Drama+Romance",
        "Animation+Family",
        "Horror+Thriller"
    ]
    print("Popular genre combinations:")
    for combo in combinations:
        print(f"  {combo}")

def main():
    print("Movie Recommendation System")
    print("=" * 40)
    
    movies, ratings = load_movie_data()
    movies_with_stats = prepare_movie_stats(movies, ratings)
    all_genres = get_all_genres(movies)
    
    print(f"Loaded {len(movies)} movies and {len(ratings)} ratings")
    
    create_analysis_report(movies, ratings, movies_with_stats)
    print_dataset_summary(movies, ratings)
    
    while True:
        print("\n" + "="*50)
        print("Main Menu")
        print("="*50)
        print("1. Get movie recommendations by genre")
        print("2. View dataset analysis report")
        print("3. Show available genres")
        print("4. Evaluate model accuracy")
        print("5. Get hybrid recommendations")
        print("6. Exit")

        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            print(f"Available genres: {', '.join(all_genres[:15])}...")
            genre_input = input("Enter genre or combination (use +): ").strip()
            
            if not genre_input:
                print("Please enter at least one genre")
                continue
            
            try:
                num_movies = input("Number of movies to show (default 10): ").strip()
                num_movies = int(num_movies) if num_movies else 10
                num_movies = max(5, min(20, num_movies))
            except ValueError:
                num_movies = 10
                print("Using default value of 10 movies")
            
            top_movies, display_name = get_genre_recommendations(genre_input, movies_with_stats, all_genres, num_movies)
            
            if top_movies is not None:
                create_recommendation_chart(top_movies, display_name)
                print_recommendations(top_movies, display_name)
                
                save = input("Save these recommendations to CSV? (y/n): ").strip().lower()
                if save == 'y':
                    filename = f"{genre_input.replace('+', '_')}_movies.csv"
                    top_movies[['title', 'genres', 'avg_rating', 'rating_count']].to_csv(filename, index=False)
                    print(f"Saved to {filename}")
        
        elif choice == '2':
            create_analysis_report(movies, ratings, movies_with_stats)
            print_dataset_summary(movies, ratings)
        
        elif choice == '3':
            print(f"All available genres ({len(all_genres)} total):")
            print("-" * 40)
            for i in range(0, len(all_genres), 4):
                print("  " + "  |  ".join(f"{genre:<15}" for genre in all_genres[i:i+4]))
            
            show_genre_combinations()
        
        elif choice == '6':
            print("Thank you for using the Movie Recommendation System!")
            break

        elif choice == '4':
            results = evaluate_recommendation_accuracy(ratings, movies_with_stats)
    
        elif choice == '5':
            try:
                user_id = int(input("Enter user ID for hybrid recommendations: "))
                genre_input = input("Enter genre: ")
                hybrid_recommendations(user_id, genre_input, movies_with_stats, ratings, all_genres)
            except ValueError:
                print("Please enter a valid user ID")

        
        else:
            print("Please enter a valid option (1-4)")

if __name__ == "__main__":
    main()