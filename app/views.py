# app/views.py

# Contains routing definitions
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from app.models import db, Product
from config import Config, access_secret
from functools import wraps

def verify_auth_token():
    #Secret Manager authentication
    try:
        stored_key = access_secret('secret_key')
        return stored_key is not None
    except Exception:
        return False

def admin_required(f):
    # Decorated function for verification
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin') or not verify_auth_token():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Index route
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Login route
def login():
    # Verify with auth token
    if request.method == 'POST':
        if not verify_auth_token():
            return render_template('login.html', error='Service error')
            
        try:
            stored_username = access_secret('db-user')     
            stored_password = access_secret('db-password')  
            
            if (request.form['username'] == stored_username and 
                request.form['password'] == stored_password):
                session['is_admin'] = True
                return redirect(url_for('index'))
        except Exception as e:
            return render_template('login.html', error='Authentication FAILURE')
            
        return render_template('login.html', error='Wrong admin credentials...')
    return render_template('login.html')

@admin_required
def add():
    # Add route (admin only)
    if request.method == 'POST':
        new_product = Product(
            id=request.form['id'],
            name=request.form['name'],
            price=float(request.form['price']),
            type=request.form['type'],
            image=request.form['image']
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@admin_required
def edit(product_id):
    #Edit route (admin only)
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.type = request.form['type']
        product.image = request.form['image']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)

@admin_required
def delete(product_id):
    # Delete route (admin only)
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('index'))
