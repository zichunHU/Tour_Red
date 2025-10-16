from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Get the absolute path for the data file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'attractions.json')

@app.route("/")
def home():
    return "Hello from the Backend!"

@app.route("/api/attractions")
def get_attractions():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            attractions = json.load(f)

        # Get query parameters
        keyword = request.args.get('keyword', type=str)
        area = request.args.get('area', type=str)
        theme = request.args.get('theme', type=str)

        # Filter logic
        if keyword:
            keyword = keyword.lower()
            attractions = [attr for attr in attractions if keyword in attr['name'].lower() or keyword in attr['description'].lower()]
        
        if area:
            attractions = [attr for attr in attractions if attr['area'] == area]

        if theme:
            attractions = [attr for attr in attractions if theme in attr['theme']]

        return jsonify(attractions)

    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

@app.route("/api/attractions/<int:attraction_id>")
def get_attraction_detail(attraction_id):
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            attractions = json.load(f)
        
        attraction = next((attr for attr in attractions if attr['id'] == attraction_id), None)
        
        if attraction:
            return jsonify(attraction)
        else:
            return jsonify({"error": "Attraction not found"}), 404
            
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
