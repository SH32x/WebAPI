# app/views.py
from flask import render_template, request, redirect, url_for, flash, current_app
from app.models import load_products, save_product

def index():
    """Handle index route"""
    try:
        products = load_products()
        return render_template('index.html', products=products)
    except Exception as e:
        current_app.logger.error(f"Error in index route: {str(e)}")
        flash("Error loading products", "error")
        return render_template('index.html', products=[])

def add():
    """Handle add route"""
    if request.method == 'POST':
        try:
            new_product = {
                'id': request.form['id'],
                'name': request.form['name'],
                'price': request.form['price'],
                'type': request.form['type'],
                'image': request.form['image']
            }
            if save_product(new_product):
                flash("Product added successfully", "success")
                return redirect(url_for('index'))
            else:
                flash("Error saving product", "error")
                return render_template('add.html')
        except Exception as e:
            current_app.logger.error(f"Error in add route: {str(e)}")
            flash("Error adding product", "error")
            return render_template('add.html')
    return render_template('add.html')