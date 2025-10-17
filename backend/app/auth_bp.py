from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth_bp', __name__)

# Hardcoded credentials for demonstration purposes
# In a real application, these would be stored securely (e.g., hashed in a database)
VALID_USERNAME = "admin"
VALID_PASSWORD = "password"

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        # For a real application, you would generate and return a JWT or session token here
        return jsonify({"message": "Login successful", "token": "fake-jwt-token"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
