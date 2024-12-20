from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

# Import other files
from signup import signup_bp
from login import login_bp
from profile import profile_bp
from favourites import favourites_bp
from reviews import reviews_bp
from anime import anime_bp


# Set app name
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# JWT Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECURE_KEY') 
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(signup_bp)
app.register_blueprint(login_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(favourites_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(anime_bp)

# API for server status
@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"message": "online"})

if __name__ == '__main__':
    app.run(debug=True)