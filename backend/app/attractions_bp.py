import os
import json
import re
import shutil
from flask import Blueprint, jsonify, request
from .data_loader import load_raw_attractions, enrich_attraction_urls, ATTRACTIONS_DATA_DIR

attractions_bp = Blueprint('attractions_bp', __name__)

def slugify(text):
    """Generate a filesystem-friendly slug from a string."""
    text = text.lower()
    text = re.sub(r'\s+', '-', text) # Replace spaces with hyphens
    text = re.sub(r'[^a-z0-9-]', '', text) # Remove non-alphanumeric characters
    return text[:50] # Truncate to 50 chars

@attractions_bp.route('/', methods=['GET'])
def get_attractions():
    try:
        backend_url = request.host_url.rstrip('/')
        raw_attractions = load_raw_attractions()
        enriched_attractions = [enrich_attraction_urls(attr, backend_url) for attr in raw_attractions]

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

@attractions_bp.route('/', methods=['POST'])
def create_attraction():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Missing required field: name"}), 400

    raw_attractions = load_raw_attractions()
    new_id = max([attr.get('id', 0) for attr in raw_attractions] + [0]) + 1
    data['id'] = new_id

    slug = slugify(data['name_en'] or data['name'])
    # Ensure slug is unique
    existing_slugs = [d.get('dir_name') for d in raw_attractions]
    if slug in existing_slugs:
        slug = f"{slug}-{new_id}"
    
    attraction_dir = os.path.join(ATTRACTIONS_DATA_DIR, slug)
    try:
        os.makedirs(attraction_dir)
        with open(os.path.join(attraction_dir, 'data.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # Create placeholder image if one is specified
        if data.get('image_url'):
            with open(os.path.join(attraction_dir, data['image_url']), 'w') as f:
                f.write('placeholder')

    except OSError as e:
        return jsonify({"error": f"Failed to create attraction directory: {e}"}), 500

    return jsonify(data), 201

@attractions_bp.route('/<int:attraction_id>', methods=['PUT'])
def update_attraction(attraction_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body cannot be empty"}), 400

    raw_attractions = load_raw_attractions()
    attraction_to_update = None
    for attr in raw_attractions:
        if attr.get('id') == attraction_id:
            attraction_to_update = attr
            break
    
    if not attraction_to_update:
        return jsonify({"error": "Attraction not found"}), 404

    attraction_dir = os.path.join(ATTRACTIONS_DATA_DIR, attraction_to_update['dir_name'])
    data_file_path = os.path.join(attraction_dir, 'data.json')

    # Load full original data to update it
    with open(data_file_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)

    original_data.update(data)

    with open(data_file_path, 'w', encoding='utf-8') as f:
        json.dump(original_data, f, ensure_ascii=False, indent=2)

    return jsonify(original_data)

@attractions_bp.route('/<int:attraction_id>', methods=['DELETE'])
def delete_attraction(attraction_id):
    raw_attractions = load_raw_attractions()
    attraction_to_delete = None
    for attr in raw_attractions:
        if attr.get('id') == attraction_id:
            attraction_to_delete = attr
            break

    if not attraction_to_delete:
        return jsonify({"error": "Attraction not found"}), 404

    attraction_dir = os.path.join(ATTRACTIONS_DATA_DIR, attraction_to_delete['dir_name'])
    
    try:
        shutil.rmtree(attraction_dir)
    except OSError as e:
        return jsonify({"error": f"Failed to delete attraction directory: {e}"}), 500

    return '', 204