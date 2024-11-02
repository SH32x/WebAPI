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
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
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

def init_db():
    """Initialize database with sample data if empty"""
    db.create_all()
    
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