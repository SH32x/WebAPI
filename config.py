# config.py

import os

class Config:
    """Configuration class for Flask application settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    # Add other configuration variables as needed
    PRODUCTS_FILE = 'products.txt'