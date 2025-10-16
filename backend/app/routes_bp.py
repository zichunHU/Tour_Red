
import os
import json
from flask import Blueprint, jsonify, request
from .data_loader import load_raw_attractions, enrich_attraction_urls, ROUTES_DATA_FILE

routes_bp = Blueprint('routes_bp', __name__)

@routes_bp.route('/', methods=['GET'])
def get_routes():
    try:
        with open(ROUTES_DATA_FILE, 'r', encoding='utf-8') as f:
            routes = json.load(f)
        return jsonify(routes)
    except FileNotFoundError:
        return jsonify({"error": "Routes data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding routes JSON"}), 500

@routes_bp.route('/<int:route_id>', methods=['GET'])
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

    except FileNotFoundError:
        return jsonify({"error": "Data file not found for routes"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON for routes"}), 500
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred in route detail: {str(e)}"}), 500
