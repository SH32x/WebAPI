# app/views.py
from flask import render_template, request, redirect, url_for, session, flash
from app.models import db, Product
from config import Config, access_secret
from functools import wraps

def verify_auth_token():
    """Verify authentication token against Secret Manager"""
    try:
        stored_key = access_secret('secret_key')
        return stored_key is not None
    except Exception:
        return False

def admin_required(f):
    """Decorator to require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin') or not verify_auth_token():
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def index():
    """Handle index route"""
    products = Product.query.all()
    return render_template('index.html', products=products)

def login():
    """Handle admin login using Secret Manager authentication"""
    if request.method == 'POST':
        if not verify_auth_token():
            return render_template('login.html', error='Authentication service unavailable')
            
        try:
            stored_username = access_secret('db-user')     
            stored_password = access_secret('db-password')  
            
            if (request.form['username'] == stored_username and 
                request.form['password'] == stored_password):
                session['is_admin'] = True
                return redirect(url_for('index'))
        except Exception as e:
            return render_template('login.html', error='Authentication failed')
            
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@admin_required
def add():
    """Handle add route (protected)"""
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
