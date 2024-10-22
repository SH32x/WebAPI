# app/views.py
# from flask import render_template
# from app import app

# @app.route('/')
# def index():
#     return render_template("index.html")


# @app.route('/about')
# def about():   
#     return render_template("about.html")

from flask import render_template, request, redirect, url_for
from app.models import load_products, save_product

def index():
    """Handle index route"""
    products = load_products()
    return render_template('index.html', products=products)

def add():
    """Handle add route"""
    if request.method == 'POST':
        new_product = {
            'id': request.form['id'],
            'name': request.form['name'],
            'price': request.form['price'],
            'type': request.form['type'],
            'image': request.form['image']
        }
        save_product(new_product)
        return redirect(url_for('index'))
    return render_template('add.html')