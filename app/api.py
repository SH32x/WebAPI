# app/api.py
# Sets up CRUD API logic, including endpoints, request formats, and authorization
from flask import Blueprint, request, jsonify
from app.models import db, Product, User, token_required

api = Blueprint('api', __name__)

def validate_product_data(data, required_fields):
    if not data:
        return False, 'No data provided'
    if not all(key in data for key in required_fields):
        return False, 'Missing required fields'
    return True, None

@api.route('/auth/login', methods=['POST'])
def login():
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
def get_products(_):
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
def get_product(_, product_id):
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
def create_product(_):
    """Create a new product"""
    data = request.get_json()
    valid, error = validate_product_data(data, ['id', 'name', 'price', 'type', 'image'])
    if not valid:
        return jsonify({'message': error}), 400
        
    product = Product(**data)
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'message': 'Product created successfully'}), 201

@api.route('/products/<product_id>', methods=['PUT'])
@token_required
def update_product(_, product_id):
    """Update an existing product"""
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'No update data provided'}), 400
        
    for key in ['name', 'price', 'type', 'image']:
        if key in data:
            setattr(product, key, data[key])
            
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@api.route('/products/<product_id>', methods=['DELETE'])
@token_required
def delete_product(_, product_id):
    """Delete a product"""
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200