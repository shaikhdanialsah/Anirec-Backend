from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import get_db_connection

# Create a blueprint for profile-related routes
profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()  # Get the user ID from the JWT token

    try:
        # Fetch user information from the database using the user_id
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, email, created_at, profile_picture, wallpaper FROM "users" WHERE id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "created_at": user[3],
                "profile_picture": user[4],
                "wallpaper": user[5]
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@profile_bp.route('/api/update-profile/<int:user_id>', methods=['PUT'])
def update_profile(user_id):
    try:
        # Fetch user information from the database using the user_id
        conn = get_db_connection()
        cur = conn.cursor()
        
        data = request.get_json()  # Get data from the request body
        username = data.get("username")
        avatar = data.get("avatar")
        background = data.get("background")

        # Perform the update query with placeholders for security
        cur.execute('''UPDATE "users" SET name = %s, profile_picture = %s, wallpaper = %s WHERE id = %s''',
                    (username, avatar, background, user_id))
        conn.commit()

        # Fetch the updated user to return the response
        cur.execute('SELECT id, name, email, created_at, profile_picture, wallpaper FROM "users" WHERE id = %s', (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            return jsonify({
                "id": user[0],
                "username": user[1],
                "email": user[2],
                "created_at": user[3],
                "profile_picture": user[4],
                "wallpaper": user[5]
            }), 200
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
