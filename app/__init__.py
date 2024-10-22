# app/__init__.py
import os
from flask import Flask
from config import Config

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    # Initialize Flask app with template folder in app directory
    app = Flask(__name__)  
    
    # Load the configuration
    app.config.from_object(config_class)
    
    # Register routes
    from app.views import index, add
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/add', 'add', add, methods=['GET', 'POST'])
    
    return app

# Create the Flask application instance
app = create_app()