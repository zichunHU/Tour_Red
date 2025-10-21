import os
import json
import re
import shutil
import time
import requests
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
import bleach

from .data_loader import load_raw_attractions, enrich_attraction_urls, ATTRACTIONS_DATA_DIR

attractions_bp = Blueprint('attractions_bp', __name__)

# --- Geocoding Configuration ---
# 警告: 请将下面的 'YOUR_AMAP_KEY' 替换为您自己的高德地图API Key。
# 为了安全，请勿将包含真实密钥的文件提交到版本控制系统。
AMAP_API_KEY = "aeaae00007b40fff8508b130084a22e6"
AMAP_GEOCODE_URL = "https://restapi.amap.com/v3/geocode/geo"

# --- Bleach HTML Sanitization Settings ---
ALLOWED_TAGS = {
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ol', 'ul', 'li', 'a', 'img', 'blockquote'
}
ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'a': ['href', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height'],
}

def geocode_address(address):
    """Convert an address to latitude and longitude using AMap API."""
    if not AMAP_API_KEY or AMAP_API_KEY == "YOUR_AMAP_KEY":
        print("Warning: AMAP_API_KEY is not set in attractions_bp.py. Geocoding will be skipped.")
        return None

    params = {
        'key': AMAP_API_KEY,
        'address': address
    }
    try:
        response = requests.get(AMAP_GEOCODE_URL, params=params)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        if data['status'] == '1' and data['geocodes']:
            location_str = data['geocodes'][0]['location']
            longitude, latitude = map(float, location_str.split(','))
            return {"latitude": latitude, "longitude": longitude}
        else:
            print(f"Geocoding failed for address '{address}'. Reason: {data.get('info')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error calling AMap API: {e}")
        return None

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

@attractions_bp.route('/<int:attraction_id>/images', methods=['POST'])
def upload_attraction_image(attraction_id):
    # Find the attraction to get its directory name
    raw_attractions = load_raw_attractions()
    attraction = next((attr for attr in raw_attractions if attr.get('id') == attraction_id), None)
    if not attraction:
        return jsonify({"error": "Attraction not found"}), 404

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Create a secure, unique filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{int(time.time())}{ext}"

        # Save the file
        attraction_dir = os.path.join(ATTRACTIONS_DATA_DIR, attraction['dir_name'])
        save_path = os.path.join(attraction_dir, unique_filename)
        file.save(save_path)

        # Construct the public URL
        backend_url = request.host_url.rstrip('/')
        image_url = f"{backend_url}/static/attractions/{attraction['dir_name']}/{unique_filename}"

        return jsonify({"imageUrl": image_url}), 201

    return jsonify({"error": "File upload failed"}), 500


@attractions_bp.route('/', methods=['POST'])
def create_attraction():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Missing required field: name"}), 400

    # --- Geocode address if present ---
    if data.get('address'):
        location = geocode_address(data['address'])
        if location:
            data['location'] = location

    raw_attractions = load_raw_attractions()
    new_id = max([attr.get('id', 0) for attr in raw_attractions] + [0]) + 1
    data['id'] = new_id

    slug = slugify(data['name_en'] or data['name'])
    # Ensure slug is unique
    existing_slugs = [d.get('dir_name') for d in raw_attractions]
    if slug in existing_slugs:
        slug = f"{slug}-{new_id}"
    
    data['dir_name'] = slug
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

    # --- Sanitize HTML content before processing ---
    if 'description' in data:
        data['description'] = bleach.clean(data['description'], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)
    if 'description_en' in data:
        data['description_en'] = bleach.clean(data['description_en'], tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)

    raw_attractions = load_raw_attractions()
    attraction_to_update = next((attr for attr in raw_attractions if attr.get('id') == attraction_id), None)
    
    if not attraction_to_update:
        return jsonify({"error": "Attraction not found"}), 404

    # --- Geocode if address is new or has changed ---
    new_address = data.get('address')
    if new_address and new_address != attraction_to_update.get('address'):
        location = geocode_address(new_address)
        if location:
            data['location'] = location

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
    attraction_to_delete = next((attr for attr in raw_attractions if attr.get('id') == attraction_id), None)

    if not attraction_to_delete:
        return jsonify({"error": "Attraction not found"}), 404

    attraction_dir = os.path.join(ATTRACTIONS_DATA_DIR, attraction_to_delete['dir_name'])
    
    try:
        shutil.rmtree(attraction_dir)
    except OSError as e:
        return jsonify({"error": f"Failed to delete attraction directory: {e}"}), 500

    return '', 204