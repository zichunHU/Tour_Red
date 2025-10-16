from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Get the absolute path for the data files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ATTRACTIONS_DATA_FILE = os.path.join(BASE_DIR, 'data', 'attractions.json')
ROUTES_DATA_FILE = os.path.join(BASE_DIR, 'data', 'routes.json')

@app.route("/")
def home():
    return "Hello from the Backend!"

# --- Attractions API --- 

@app.route("/api/attractions")
def get_attractions():
    try:
        with open(ATTRACTIONS_DATA_FILE, 'r', encoding='utf-8') as f:
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
        return jsonify({"error": "Attractions data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

@app.route("/api/attractions/<int:attraction_id>")
def get_attraction_detail(attraction_id):
    try:
        with open(ATTRACTIONS_DATA_FILE, 'r', encoding='utf-8') as f:
            attractions = json.load(f)
        
        attraction = next((attr for attr in attractions if attr['id'] == attraction_id), None)
        
        if attraction:
            return jsonify(attraction)
        else:
            return jsonify({"error": "Attraction not found"}), 404
            
    except FileNotFoundError:
        return jsonify({"error": "Attractions data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

# --- Routes API --- 

@app.route("/api/routes")
def get_routes():
    try:
        with open(ROUTES_DATA_FILE, 'r', encoding='utf-8') as f:
            routes = json.load(f)
        return jsonify(routes)
    except FileNotFoundError:
        return jsonify({"error": "Routes data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

@app.route("/api/routes/<int:route_id>")
def get_route_detail(route_id):
    try:
        with open(ROUTES_DATA_FILE, 'r', encoding='utf-8') as f:
            routes = json.load(f)
        with open(ATTRACTIONS_DATA_FILE, 'r', encoding='utf-8') as f:
            all_attractions = json.load(f)

        route = next((r for r in routes if r['id'] == route_id), None)

        if not route:
            return jsonify({"error": "Route not found"}), 404

        # Enrich route with full attraction details
        attraction_details = []
        for attr_id in route.get('attraction_ids', []):
            detail = next((attr for attr in all_attractions if attr['id'] == attr_id), None)
            if detail:
                attraction_details.append(detail)
        
        route['attractions'] = attraction_details
        
        return jsonify(route)

    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
