from flask import Blueprint, jsonify, request
from database import get_db_connection
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

anime_bp = Blueprint('anime', __name__)

#Get anime
def get_anime_data():
    try:
        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all anime records
        cursor.execute("SELECT * FROM anime JOIN anime_scores ON anime.anime_id = anime_scores.anime_id ORDER BY score DESC")
        anime_data = cursor.fetchall()

        # Optional: Convert the data to a dictionary if needed
        column_names = [desc[0] for desc in cursor.description]
        anime_data_dict = [dict(zip(column_names, row)) for row in anime_data]

        return anime_data_dict

    except Exception as e:
        raise RuntimeError(f"Error fetching anime data from the database: {e}")
    
    finally:
        # Close the database connection
        cursor.close()
        conn.close()


anime_data = get_anime_data()

# Preprocess descriptions for recommender
for anime in anime_data:
    anime['processed_description'] = re.sub(r'\W+', ' ', anime.get('description', '').lower().strip())  # Ensure valid description
    anime['processed_title'] = re.sub(r'\W+', ' ', anime.get('title', '').lower().strip())  # Preprocess titles
    anime['processed_genres'] = re.sub(r'\W+', ' ', anime.get('genres', '').lower().strip())  # Preprocess genres

# TF-IDF Vectorizers for each feature
desc_vectorizer = TfidfVectorizer(stop_words='english')
title_vectorizer = TfidfVectorizer(stop_words='english')
genre_vectorizer = TfidfVectorizer(stop_words='english')

# Compute TF-IDF matrices
desc_tfidf_matrix = desc_vectorizer.fit_transform([anime['processed_description'] for anime in anime_data])
title_tfidf_matrix = title_vectorizer.fit_transform([anime['processed_title'] for anime in anime_data])
genre_tfidf_matrix = genre_vectorizer.fit_transform([anime['processed_genres'] for anime in anime_data])


# Anime Recommender System
@anime_bp.route('/api/recommend', methods=['GET'])
def recommend_anime():
    user_input = request.args.get('anime', '').strip().lower()

    if not user_input:
        return jsonify({"error": "Anime title is required"}), 400

    # Find the input anime
    anime_index = next((index for index, anime in enumerate(anime_data)
                        if anime['title'].lower() == user_input or anime.get('english_title', '').lower() == user_input), None)

    if anime_index is None:
        return jsonify({"error": "Anime not found"}), 404

    input_anime = anime_data[anime_index]

    # Calculate similarity scores
    desc_similarities = cosine_similarity(desc_tfidf_matrix[anime_index], desc_tfidf_matrix).flatten()
    title_similarities = cosine_similarity(title_tfidf_matrix[anime_index], title_tfidf_matrix).flatten()
    genre_similarities = cosine_similarity(genre_tfidf_matrix[anime_index], genre_tfidf_matrix).flatten()

    # Combine similarities with weights
    combined_similarities = (0.3 * desc_similarities) + (0.4 * title_similarities) + (0.3 * genre_similarities)

    # Add combined similarity scores to anime data
    for idx, anime in enumerate(anime_data):
        anime['similarity'] = float(combined_similarities[idx])  # Convert to float for JSON serialization

    # Filter and sort recommendations
    recommended_animes = sorted(
        [
            anime for idx, anime in enumerate(anime_data)
            if idx != anime_index and  # Exclude the input anime itself
               anime.get('genres', '').split(',')[0].strip().lower() == input_anime.get('genres', '').split(',')[0].strip().lower() 
        ],
        key=lambda x: x['similarity'], reverse=True
    )[:20]  # Top 20 recommendations

    return jsonify(recommended_animes=recommended_animes)


# API to get random anime
@anime_bp.route('/api/random', methods=['GET'])
def get_random_anime():
    genre = request.args.get('genre', 'All Genre').strip().lower()

    if genre != 'all genre':
        anime_genre = [
            anime for anime in anime_data 
            if genre in [g.strip().lower() for g in anime.get('genres', '').split(',')] 
        ]
        filtered_anime = sorted(anime_genre, key=lambda x: x.get('score', 0), reverse=True)[:100]
    else:
        # filtered_anime = [anime for anime in anime_data if anime.get('score', 0) > 7]
        filtered_anime = sorted(anime_data, key=lambda x: x.get('score', 0), reverse=True)[:300]

    if not filtered_anime:
        return jsonify(anime=None)

    random_anime = random.choice(filtered_anime)
    return jsonify(anime=random_anime)

# API to return genres and their counts
@anime_bp.route('/api/genres', methods=['GET'])
def get_genre_stats():
    genre_count = {}

    for anime in anime_data:
        genres = [g.strip() for g in anime.get('genres', '').split(',')]
        for genre in genres:
            genre_count[genre] = genre_count.get(genre, 0) + 1

    unique_genres = len(genre_count)

    return jsonify({
        'unique_genres': unique_genres,
        'genre_count': genre_count
    })

# API to get a list of all anime
@anime_bp.route('/api/anime', methods=['GET'])
def get_anime_list():
    return jsonify(anime_list=anime_data)

# API to get top 100 anime based on score
@anime_bp.route('/api/anime/top100', methods=['GET'])
def get_top_100_anime():
    # Sort anime by score in descending order and take the top 100
    top_100_anime = sorted(anime_data, key=lambda x: x.get('score', 0), reverse=True)[:100]
    return jsonify(top_100_anime=top_100_anime)

# API to get anime by genre
@anime_bp.route('/api/anime-genre/<string:genre>', methods=['GET'])
def get_anime_by_genre(genre):
    # Normalize the input genre
    genre = genre.strip().lower()

    # Filter anime based on genre
    filtered_anime = [
        anime for anime in anime_data
        if genre in [g.strip().lower() for g in anime.get('genres', '').split(',')]
    ]

    # If no anime is found for the genre, return a message
    if not filtered_anime:
        return jsonify({
            'genre': genre,
            'anime_list': [],
            'message': 'No anime found for this genre'
        })

    # Return the filtered anime list
    return jsonify({
        'genre': genre,
        'anime_list': filtered_anime
    })

# API to get anime by ID
@anime_bp.route('/api/anime/<int:anime_id>', methods=['GET'])
def get_anime_by_id(anime_id):
    anime = next((anime for anime in anime_data if anime['anime_id'] == anime_id), None)
    if anime:
        return jsonify(anime=anime)
    else:
        return jsonify(error="Anime not found"), 404