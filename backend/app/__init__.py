
from flask import Flask, send_from_directory
from flask_cors import CORS
import os

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # --- Path for static files ---
    # This needs to point to the 'attractions' directory inside 'data'
    attractions_data_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'attractions')

    @app.route('/static/attractions/<path:path>')
    def serve_attraction_image(path):
        return send_from_directory(attractions_data_dir, path)

    # --- Register Blueprints ---
    from . import attractions_bp
    app.register_blueprint(attractions_bp.attractions_bp, url_prefix='/api/attractions')

    from . import routes_bp
    app.register_blueprint(routes_bp.routes_bp, url_prefix='/api/routes')

    @app.route("/")
    def home():
        return "Hello from the modular Flask backend!"

    return app
