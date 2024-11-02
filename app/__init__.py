# app/__init__.py
from flask import Flask
from config import Config
from app.models import db, init_db

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)
    
    # Explicitly set secret key
    if not app.config['SECRET_KEY']:
        raise RuntimeError(
            'SECRET_KEY not set. Ensure secret_key is properly configured in Google Cloud Secret Manager.'
        )
    
    # Initialize extensions
    db.init_app(app)
    
    # Register routes
    from app.views import index, add, login
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/add', 'add', add, methods=['GET', 'POST'])
    app.add_url_rule('/admin/login', 'login', login, methods=['GET', 'POST'])
    
    # Register API blueprint
    from app.api import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Initialize database
    with app.app_context():
        init_db()
    
    return app

app = create_app()