# app/__init__.py
# Initializes the app, defines routes, api, database on loadup
from flask import Flask
from config import Config
from app.models import db, init_db

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)
    
    # Check for secret key
    if not app.config['SECRET_KEY']:
        raise RuntimeError(
            'SECRET_KEY not set, please configure secret_key in the Google Cloud Secret Manager.'
        )
    
    # Initialize extensions
    db.init_app(app)
    
    # Register routes
    from app.views import index, add, login, edit, delete
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/add', 'add', add, methods=['GET', 'POST'])
    app.add_url_rule('/admin/login', 'login', login, methods=['GET', 'POST'])
    app.add_url_rule('/edit/<product_id>', 'edit', edit, methods=['GET', 'POST'])
    app.add_url_rule('/delete/<product_id>', 'delete', delete, methods=['POST'])
    
    # Register API blueprint
    from app.api import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Initialize database
    with app.app_context():
        init_db()
    
    return app

app = create_app()