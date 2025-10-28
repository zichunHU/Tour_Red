import os
import json
import math
from flask import Blueprint, jsonify, request
from .data_loader import load_raw_attractions, enrich_attraction_urls, ROUTES_DATA_FILE

routes_bp = Blueprint('routes_bp', __name__)

def read_routes_file():
    """Helper to read the routes data file."""
    try:
        with open(ROUTES_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] # Return empty list if file doesn't exist or is invalid

def write_routes_file(data):
    """Helper to write to the routes data file."""
    with open(ROUTES_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def calculate_distance(loc1, loc2):
    """Calculate the Haversine distance between two lat/lon points."""
    R = 6371  # Earth radius in kilometers
    lat1, lon1 = math.radians(loc1['latitude']), math.radians(loc1['longitude'])
    lat2, lon2 = math.radians(loc2['latitude']), math.radians(loc2['longitude'])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

@routes_bp.route('/', methods=['GET'])
def get_routes():
    routes = read_routes_file()
    return jsonify(routes)

@routes_bp.route('/<int:route_id>', methods=['GET'])
def get_route_detail(route_id):
    try:
        backend_url = request.host_url.rstrip('/')
        routes = read_routes_file()
        raw_attractions = load_raw_attractions()
        enriched_attractions = [enrich_attraction_urls(attr, backend_url) for attr in raw_attractions]

        route = next((r for r in routes if r.get('id') == route_id), None)

        if not route:
            return jsonify({"error": "Route not found"}), 404

        attraction_details = []
        for attr_id in route.get('attraction_ids', []):
            detail = next((attr for attr in enriched_attractions if attr.get('id') == attr_id), None)
            if detail:
                attraction_details.append(detail)
        
        route['attractions'] = attraction_details
        return jsonify(route)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred in route detail: {str(e)}"}), 500

@routes_bp.route('/generate', methods=['POST'])
def generate_custom_route():
    data = request.get_json()
    if not data or 'attraction_ids' not in data or len(data['attraction_ids']) < 2:
        return jsonify({"error": "Please provide at least two attraction IDs."}), 400

    backend_url = request.host_url.rstrip('/')
    all_attractions = load_raw_attractions()
    
    # Filter to get only the selected attractions
    selected_attractions = [attr for attr in all_attractions if attr['id'] in data['attraction_ids']]

    if len(selected_attractions) < 2:
        return jsonify({"error": "Not enough valid attractions found to create a route."}), 400

    # Nearest-neighbor algorithm to sort attractions
    unvisited = list(selected_attractions)
    ordered_route = []
    current_attraction = unvisited.pop(0)
    ordered_route.append(current_attraction)

    while unvisited:
        nearest_attraction = min(unvisited, key=lambda attr: calculate_distance(current_attraction['location'], attr['location']))
        ordered_route.append(nearest_attraction)
        unvisited.remove(nearest_attraction)
        current_attraction = nearest_attraction

    # Enrich URLs for the final ordered list
    enriched_ordered_route = [enrich_attraction_urls(attr, backend_url) for attr in ordered_route]

    # Create a temporary route object to send back
    custom_route = {
        "name": "我的专属定制路线",
        "description": "这是一条根据您的兴趣和选择生成的个性化路线。",
        "attractions": enriched_ordered_route
    }

    return jsonify(custom_route)

@routes_bp.route('/', methods=['POST'])
def create_route():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Missing required field: name"}), 400

    routes = read_routes_file()
    new_id = max([r.get('id', 0) for r in routes] + [0]) + 1
    data['id'] = new_id
    
    routes.append(data)
    write_routes_file(routes)
    
    return jsonify(data), 201

@routes_bp.route('/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body cannot be empty"}), 400

    routes = read_routes_file()
    route_to_update = None
    updated_routes = []
    for route in routes:
        if route.get('id') == route_id:
            route.update(data)
            route_to_update = route
        updated_routes.append(route)

    if not route_to_update:
        return jsonify({"error": "Route not found"}), 404

    write_routes_file(updated_routes)
    return jsonify(route_to_update)

@routes_bp.route('/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    routes = read_routes_file()
    route_exists = any(r.get('id') == route_id for r in routes)
    if not route_exists:
        return jsonify({"error": "Route not found"}), 404

    updated_routes = [r for r in routes if r.get('id') != route_id]
    write_routes_file(updated_routes)

    return '', 204