from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
import psycopg2
from database import get_db_connection

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('name', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    password_hash = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO "users" (email, name, password) VALUES (%s, %s, %s)',
                    (email, username, password_hash))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "User registered successfully"}), 201
    except psycopg2.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
