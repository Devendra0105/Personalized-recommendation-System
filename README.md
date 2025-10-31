Personalized Movie Recommendation System

This is a Python-based movie recommendation system that suggests movies according to a user’s preferred genres and viewing patterns.
It uses both content-based filtering and collaborative filtering, and also includes a hybrid model that combines both approaches for better recommendations.

Overview

The goal of this project is to help users find movies they might enjoy by analyzing the MovieLens dataset.
It includes a simple command-line interface where you can choose genres, get recommendations, view reports, and check how well the model performs.

What You Can Do

Get movie recommendations by genre or mix of genres

Generate hybrid recommendations based on user similarity + genres

Visualize the dataset (top genres, rating patterns, user activity, etc.)

Check model accuracy with RMSE, MAE, and Precision@K

Save recommended movies into CSV files

Tech Stack

Language: Python

Libraries: pandas, numpy, matplotlib, scikit-learn

Algorithm: Cosine Similarity (for collaborative filtering)

Dataset: MovieLens (small version)

File Structure
Personalized-recommendation-System/
│
├── main.py                   # Main entry point with menu options
├── data_loader.py            # Loads and prepares movie and rating data
├── recommender.py            # Handles genre-based recommendations
├── hybrid_recommeder.py      # Combines content-based and collaborative filtering
├── evaluator.py              # Evaluation metrics (RMSE, MAE, Precision@K)
├── visualizer.py             # Charts, graphs, and analysis reports
├── movie_analysis_report.png # Sample visualization
└── ml-latest-small/          # MovieLens dataset

Dataset

The project uses the MovieLens Latest Small Dataset

Visual Report

When you generate the analysis report, it creates a file named movie_analysis_report.png showing:
Rating distribution
Top movie genres
User activity levels
Highest-rated movies


Possible Improvements
Build a simple web interface using Streamlit or Flask
Try advanced collaborative filtering (Matrix Factorization, SVD, etc.)
Include user profile data for personalized suggestions
Use larger datasets for more accurate recommendations

movies.csv → movie titles, IDs, and genres

ratings.csv → user ratings for movies
