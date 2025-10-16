from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# --- Paths and Directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ATTRACTIONS_DATA_DIR = os.path.join(DATA_DIR, 'attractions')
ROUTES_DATA_FILE = os.path.join(DATA_DIR, 'routes.json')

# --- Helper Function to Load All Attractions ---
def load_all_attractions():
    """
    Scans the attractions directory, loads each attraction's data,
    and enriches it with a full image URL.
    """
    all_attractions = []
    if not os.path.exists(ATTRACTIONS_DATA_DIR):
        return all_attractions

    for attraction_dir_name in os.listdir(ATTRACTIONS_DATA_DIR):
        attraction_path = os.path.join(ATTRACTIONS_DATA_DIR, attraction_dir_name)
        if os.path.isdir(attraction_path):
            data_file_path = os.path.join(attraction_path, 'data.json')
            if os.path.exists(data_file_path):
                try:
                    with open(data_file_path, 'r', encoding='utf-8') as f:
                        attraction_data = json.load(f)
                        # Enrich with the directory name for URL generation
                        attraction_data['dir_name'] = attraction_dir_name
                        # Enrich with the full image URL
                        attraction_data['image_url'] = f"/static/attractions/{attraction_dir_name}/{attraction_data.get('image_url', '')}"
                        all_attractions.append(attraction_data)
                except (json.JSONDecodeError, IOError):
                    # Skip corrupted or unreadable files
                    continue
    return all_attractions

# --- Static File Server for Attraction Images ---
@app.route('/static/attractions/<path:path>')
def serve_attraction_image(path):
    """Serves files from the dynamic attractions data directory."""
    return send_from_directory(ATTRACTIONS_DATA_DIR, path)

# --- Main Routes ---
@app.route("/")
def home():
    return "Hello from the Backend! Data structure has been refactored."

# --- Attractions API ---
@app.route("/api/attractions")
def get_attractions():
    try:
        attractions = load_all_attractions()

        # Get query parameters
        keyword = request.args.get('keyword', type=str)
        area = request.args.get('area', type=str)
        theme = request.args.get('theme', type=str)

        # Filter logic
        if keyword:
            keyword = keyword.lower()
            attractions = [attr for attr in attractions if keyword in attr['name'].lower() or keyword in attr['description'].lower()]
        
        if area:
            attractions = [attr for attr in attractions if attr.get('area') == area]

        if theme:
            attractions = [attr for attr in attractions if theme in attr.get('theme', [])]

        return jsonify(attractions)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route("/api/attractions/<int:attraction_id>")
def get_attraction_detail(attraction_id):
    try:
        all_attractions = load_all_attractions()
        attraction = next((attr for attr in all_attractions if attr.get('id') == attraction_id), None)
        
        if attraction:
            return jsonify(attraction)
        else:
            return jsonify({"error": "Attraction not found"}), 404
            
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

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
        
        all_attractions = load_all_attractions()

        route = next((r for r in routes if r.get('id') == route_id), None)

        if not route:
            return jsonify({"error": "Route not found"}), 404

        # Enrich route with full attraction details
        attraction_details = []
        for attr_id in route.get('attraction_ids', []):
            detail = next((attr for attr in all_attractions if attr.get('id') == attr_id), None)
            if detail:
                attraction_details.append(detail)
        
        route['attractions'] = attraction_details
        
        return jsonify(route)

    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)