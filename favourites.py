from flask import Blueprint, jsonify, request
from database import get_db_connection

favourites_bp = Blueprint('favourites', __name__)

# Add Anime to Favourites
@favourites_bp.route('/api/add-favourites/<int:user_id>/<int:anime_id>', methods=['POST'])
def addFavourites(user_id, anime_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if the anime is already in the user's favourites (optional)
        cur.execute('SELECT * FROM "favourites" WHERE user_id = %s AND anime_id = %s', (user_id, anime_id))
        existing_fav = cur.fetchone()
        
        if existing_fav:
            return jsonify({"error": "Anime is already in your favourites"}), 400
        
        # Insert into favourites table
        cur.execute('INSERT INTO "favourites" (user_id, anime_id) VALUES (%s, %s)', (user_id, anime_id))
        conn.commit()
        
        cur.close()
        conn.close()
        
        return jsonify({"message": "Anime added to favourites successfully!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to add to favourites"}), 500

# List Favourites for User ID
@favourites_bp.route('/api/favourites/<int:user_id>', methods=['GET'])
def getFavourites(user_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cur = conn.cursor()

        # Get all favourite anime for the user
        cur.execute('SELECT id, "favourites".anime_id, title, score, main_picture, genres FROM "favourites" JOIN "anime" ON "favourites".anime_id = "anime".anime_id WHERE user_id = %s ORDER BY id DESC', (user_id,))
        favourites = cur.fetchall()

        # Format the response to include more details about each favourite anime
        fav_list = [
            {
                "anime_id": fav[1],
                "title": fav[2],
                "score": fav[3],
                "main_picture": fav[4],
                "genres": fav[5],
            } for fav in favourites
        ]

        cur.close()
        conn.close()

        return jsonify({"favourites": fav_list}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to fetch favourites"}), 500

# Remove Anime from Favourites
@favourites_bp.route('/api/remove-favourites/<int:user_id>/<int:anime_id>', methods=['POST'])
def deleteFavourites(user_id, anime_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if the anime is already in the user's favourites
        cur.execute('SELECT * FROM "favourites" WHERE user_id = %s AND anime_id = %s', (user_id, anime_id))
        existing_fav = cur.fetchone()

        if not existing_fav:
            return jsonify({"error": "Anime is not in your favourites"}), 400

        # Remove from favourites table
        cur.execute('DELETE FROM "favourites" WHERE user_id = %s AND anime_id = %s', (user_id, anime_id))
        conn.commit()

        cur.close()
        conn.close()
        
        return jsonify({"message": "Anime removed from favourites successfully!"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred while removing from favourites"}), 500
