
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import re

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# --- Paths and Directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
ATTRACTIONS_DATA_DIR = os.path.join(DATA_DIR, 'attractions')
ROUTES_DATA_FILE = os.path.join(DATA_DIR, 'routes.json')

# --- Data Loading and Enrichment Helpers ---
def load_raw_attractions():
    """Scans the attractions directory and loads the raw data from each data.json."""
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
                        attraction_data['dir_name'] = attraction_dir_name
                        all_attractions.append(attraction_data)
                except (json.JSONDecodeError, IOError):
                    continue
    return all_attractions

def enrich_attraction_urls(attraction, backend_url):
    """Enriches all image URLs in a single attraction object to be absolute."""
    dir_name = attraction.get('dir_name')
    if not dir_name:
        return attraction

    base_image_path = f"{backend_url}/static/attractions/{dir_name}/"

    # 1. Enrich main image_url
    if 'image_url' in attraction and not str(attraction['image_url']).startswith('http'):
        attraction['image_url'] = f"{base_image_path}{attraction['image_url']}"

    # 2. Enrich markdown image urls
    def enrich_markdown(markdown_text):
        if not markdown_text: return markdown_text
        
        def replacer(match):
            alt_text = match.group(1)
            relative_path = match.group(2)
            return f'![{alt_text}]({base_image_path}{relative_path})'

        return re.sub(r'!\[(.*?)\]\((?!https?://)(.*?)\)', replacer, markdown_text)

    if 'description' in attraction:
        attraction['description'] = enrich_markdown(attraction['description'])
    if 'description_en' in attraction:
        attraction['description_en'] = enrich_markdown(attraction['description_en'])
    
    return attraction

# --- Static File Server for Attraction Images ---
@app.route('/static/attractions/<path:path>')
def serve_attraction_image(path):
    return send_from_directory(ATTRACTIONS_DATA_DIR, path)

# --- Main Routes ---
@app.route("/")
def home():
    return "Hello from the Backend! Using consistent absolute URL generation."

# --- Attractions API ---
@app.route("/api/attractions")
def get_attractions():
    try:
        backend_url = request.host_url.rstrip('/')
        raw_attractions = load_raw_attractions()
        enriched_attractions = [enrich_attraction_urls(attr, backend_url) for attr in raw_attractions]

        # Filtering logic
        keyword = request.args.get('keyword', type=str)
        area = request.args.get('area', type=str)
        theme = request.args.get('theme', type=str)

        if keyword:
            keyword = keyword.lower()
            enriched_attractions = [attr for attr in enriched_attractions if keyword in attr['name'].lower() or keyword in attr.get('description','').lower()]
        if area:
            enriched_attractions = [attr for attr in enriched_attractions if attr.get('area') == area]
        if theme:
            enriched_attractions = [attr for attr in enriched_attractions if theme in attr.get('theme', [])]

        return jsonify(enriched_attractions)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route("/api/attractions/<int:attraction_id>")
def get_attraction_detail(attraction_id):
    try:
        backend_url = request.host_url.rstrip('/')
        raw_attractions = load_raw_attractions()
        attraction = next((attr for attr in raw_attractions if attr.get('id') == attraction_id), None)

        if not attraction:
            return jsonify({"error": "Attraction not found"}), 404

        enriched_attraction = enrich_attraction_urls(attraction, backend_url)
        return jsonify(enriched_attraction)

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
        backend_url = request.host_url.rstrip('/')
        with open(ROUTES_DATA_FILE, 'r', encoding='utf-8') as f:
            routes = json.load(f)
        
        raw_attractions = load_raw_attractions()
        enriched_attractions = [enrich_attraction_urls(attr, backend_url) for attr in raw_attractions]

        route = next((r for r in routes if r.get('id') == route_id), None)

        if not route:
            return jsonify({"error": "Route not found"}), 404

        # Enrich route with full attraction details
        attraction_details = []
        for attr_id in route.get('attraction_ids', []):
            detail = next((attr for attr in enriched_attractions if attr.get('id') == attr_id), None)
            if detail:
                attraction_details.append(detail)
        
        route['attractions'] = attraction_details
        
        return jsonify(route)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
