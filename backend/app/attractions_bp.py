
from flask import Blueprint, jsonify, request
from .data_loader import load_raw_attractions, enrich_attraction_urls

attractions_bp = Blueprint('attractions_bp', __name__)

@attractions_bp.route('/', methods=['GET'])
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
        # In a real app, you'd want more specific error logging
        return jsonify({"error": f"An unexpected error occurred in attractions: {str(e)}"}), 500

@attractions_bp.route('/<int:attraction_id>', methods=['GET'])
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
        return jsonify({"error": f"An unexpected error occurred in attraction detail: {str(e)}"}), 500
