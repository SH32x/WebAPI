# app/api.py
from flask import Blueprint, request, jsonify
from app.models import db, Product, User, token_required

api = Blueprint('api', __name__)

@api.route('/auth/register', methods=['POST'])
def register():
    """Register a new API user"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
        
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    """Login and receive authentication token"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
        
    token = user.generate_token()
    return jsonify({'token': token}), 200

@api.route('/products', methods=['GET'])
@token_required
def get_products(current_user):
    """Get all products"""
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'type': p.type,
        'image': p.image
    } for p in products]), 200

@api.route('/products/<product_id>', methods=['GET'])
@token_required
def get_product(current_user, product_id):
    """Get a specific product"""
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'type': product.type,
        'image': product.image
    }), 200

@api.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    """Create a new product"""
    data = request.get_json()
    
    if not all(key in data for key in ['id', 'name', 'price', 'type', 'image']):
        return jsonify({'message': 'Missing required fields'}), 400
        
    product = Product(
        id=data['id'],
        name=data['name'],
        price=data['price'],
        type=data['type'],
        image=data['image']
    )
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'message': 'Product created successfully'}), 201

@api.route('/products/<product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    """Update an existing product"""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'type' in data:
        product.type = data['type']
    if 'image' in data:
        product.image = data['image']
        
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@api.route('/products/<product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    """Delete a product"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200