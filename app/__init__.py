# app/__init__.py
import os
from flask import Flask
from config import Config
from app.models import db, init_db

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register routes
    from app.views import index, add
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/add', 'add', add, methods=['GET', 'POST'])
    
    # Register API blueprint
    from app.api import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Initialize database
    with app.app_context():
        init_db()
    
    return app

# Create the Flask application instance
app = create_app()