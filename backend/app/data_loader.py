
import os
import json
import re

# Define paths relative to this file's location
# This makes the data loader more portable
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(BACKEND_DIR, 'data')
ATTRACTIONS_DATA_DIR = os.path.join(DATA_DIR, 'attractions')
ROUTES_DATA_FILE = os.path.join(DATA_DIR, 'routes.json')

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
