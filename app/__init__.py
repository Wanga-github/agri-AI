from flask import Flask
from flask_cors import CORS
from config.config import config
from config.logging_config import setup_logging

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Enable CORS
    CORS(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    from app.routes.api import api_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(dashboard_bp)
    
    return app