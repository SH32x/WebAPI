# Handles users and authentication, contains classes to represent users
# Contains variables for each class, including id, passwords, credentials
# Potentially has additional classes for departments, roles, etc. 

# app/models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
from flask import current_app, request, jsonify
from functools import wraps

db = SQLAlchemy()

class User(db.Model):
    """User model for API authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        """Generate JWT token for API authentication"""
        token = jwt.encode(
            {'user_id': self.id, 'exp': datetime.utcnow() + timedelta(hours=24)},
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
        return token

class Product(db.Model):
    """Product model for database operations"""
    id = db.Column(db.String(64), primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(256), nullable=False)

def load_products():
    """
    Load all products from the database
    Returns:
        list: List of Product objects
    """
    try:
        products = Product.query.all()
        return products
    except Exception as e:
        current_app.logger.error(f"Error loading products: {str(e)}")
        return []

def save_product(product_data):
    """
    Save a new product to the database
    Args:
        product_data (dict): Dictionary containing product information
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        product = Product(
            id=product_data['id'],
            name=product_data['name'],
            price=float(product_data['price']),
            type=product_data['type'],
            image=product_data['image']
        )
        db.session.add(product)
        db.session.commit()
        return True
    except Exception as e:
        current_app.logger.error(f"Error saving product: {str(e)}")
        db.session.rollback()
        return False

def token_required(f):
    """Decorator to require valid token for API access"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
            
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

# Initialize database tables
def init_db():
    """Initialize database with sample data if empty"""
    try:
        with current_app.app_context():
            db.create_all()
            
            # Only add sample data if no products exist
            if Product.query.count() == 0:
                sample_products = [
                    {
                        'id': '1',
                        'name': 'Product A',
                        'price': 10.99,
                        'type': 'Type 1',
                        'image': 'https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f'
                    },
                    {
                        'id': '2',
                        'name': 'Product B',
                        'price': 15.49,
                        'type': 'Type 2',
                        'image': 'https://images.unsplash.com/photo-1567306226416-28f0efdc88ce'
                    }
                ]
                
                for product_data in sample_products:
                    product = Product(**product_data)
                    db.session.add(product)
                
                db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error initializing database: {str(e)}")
        db.session.rollback()