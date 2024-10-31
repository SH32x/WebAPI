# .vscode\launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask: Development",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "runpoint.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1",
                "SECRET_KEY": "SECRET_KEY",
                "DATABASE_URL": "mysql+pymysql://$(DB_USER):$(DB_PASSWORD)@localhost/$(DB_NAME)"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        },
        {
            "name": "Flask: Production",
            "type": "debugpy",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "runpoint.py",
                "FLASK_ENV": "production",
                "FLASK_DEBUG": "0",
                "SECRET_KEY": "SECRET_KEY",
                "DATABASE_URL": "mysql+pymysql://$(DB_USER):$(DB_PASSWORD)@/$(DB_NAME)?unix_socket=/cloudsql/webapi-439022:northamerica-northeast2:t345db"
            },
            "args": [
                "run",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        }
    ]
}
```

# app.yaml

```yaml
# Gcloud yaml

runtime: python39
entrypoint: gunicorn -b :$PORT runpoint:app

env_variables:
  FLASK_ENV: 'production'
  FLASK_DEBUG: '0'
  SECRET_KEY: 'SECRET_KEY'  
  DATABASE_URL: >-
    mysql+pymysql://$(DB_USER):$(DB_PASSWORD)@/$(DB_NAME)
    ?unix_socket=/cloudsql/webapi-439022:northamerica-northeast2:t345db

instance_class: F1

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
  target_throughput_utilization: 0.6

handlers:
- url: /static
  static_dir: app/static
- url: /.*
  script: auto
  secure: always  # Enforces HTTPS


```

# app\__init__.py

```py
# app/__init__.py
import os
from flask import Flask
from config import Config
from app.models import db

def create_app(config_class=Config):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Register routes
    from app.views import index, add
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/add', 'add', add, methods=['GET', 'POST'])
    
    # Register API blueprint
    from app.api import api
    app.register_blueprint(api, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

# Create the Flask application instance
app = create_app()
```

# app\api.py

```py
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
```

# app\forms.py

```py
# app/forms.py
# from flask_wtf import FlaskForm
# from wtforms import StringField, DecimalField, SubmitField
# from wtforms.validators import DataRequired

# class ProductForm(FlaskForm):
#     """Form class for product creation"""
#     id = StringField('Product ID', validators=[DataRequired()])
#     name = StringField('Product Name', validators=[DataRequired()])
#     price = StringField('Price', validators=[DataRequired()])
#     type = StringField('Product Type', validators=[DataRequired()])
#     image = StringField('Image URL', validators=[DataRequired()])
#     submit = SubmitField('Add Product')
```

# app\models.py

```py
# Handles users and authentication, contains classes to represent users
# Contains variables for each class, including id, passwords, credentials
# Potentially has additional classes for departments, roles, etc. 

# app/models.py
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt
import jwt
from flask import current_app
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
```

# app\static\styles.css

```css
/* app/static/styles.css */

body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
}

header {
    background-color: #343a40;
    color: white;
    padding: 10px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}

header h1 {
    margin: 0;
}

.add-product-button, .back-button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 5px;
    transition: background-color 0.3s ease;
}

.add-product-button:hover, .back-button:hover {
    background-color: #0056b3;
}

main {
    padding: 20px;
}

.product-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20px;
}

.product {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 220px;
    text-align: center;
    transition: transform 0.2s;
}

.product:hover {
    transform: scale(1.05);
}

.product img {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    max-width: 100%;
    height: 150px;
    object-fit: cover;
}

.product-info {
    padding: 10px;
}

.product h2 {
    font-size: 1.2em;
    margin: 10px 0;
}

.price {
    color: #28a745;
    font-weight: bold;
}

.type {
    color: #6c757d;
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
}

form label, form input {
    margin: 5px;
}

footer {
    background-color: #343a40;
    color: white;
    text-align: center;
    padding: 10px 0;
    position: fixed;
    width: 100%;
    bottom: 0;
}

```

# app\templates\add.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Add Product</title>
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='styles.css') }}"
    />
  </head>
  <body>
    <header>
      <div class="header-content">
        <h1>Add a New Product</h1>
        <a href="{{ url_for('index') }}" class="back-button"
          >Back to Products</a
        >
      </div>
    </header>
    <main>
      <form action="{{ url_for('add') }}" method="post">
        <label for="id">ID:</label>
        <input type="text" id="id" name="id" required /><br />
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required /><br />
        <label for="price">Price:</label>
        <input type="text" id="price" name="price" required /><br />
        <label for="type">Type:</label>
        <input type="text" id="type" name="type" required /><br />
        <label for="image">Image URL:</label>
        <input type="text" id="image" name="image" required /><br />
        <input type="submit" value="Add Product" />
      </form>
    </main>
    <footer>
      <p>&copy; 2024 SOFE Studio, SH32x, add.html.</p>
    </footer>
  </body>
</html>

```

# app\templates\index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Online Shopping</title>
    <link
      rel="stylesheet"
      href="{{ url_for('static', filename='styles.css') }}"
    />
  </head>
  <body>
    <header>
      <div class="header-content">
        <h1>Online Shopping</h1>
        <a href="{{ url_for('add') }}" class="add-product-button"
          >Add New Product</a
        >
      </div>
    </header>
    <main>
      <div class="product-list">
        {% for product in products %}
        <div class="product">
          <img src="{{ product.image }}" alt="{{ product.name }}" />
          <div class="product-info">
            <h2>{{ product.name }}</h2>
            <p class="price">Price: ${{ product.price }}</p>
            <p class="type">Type: {{ product.type }}</p>
          </div>
        </div>
        {% endfor %}
      </div>
    </main>
    <footer>
      <p>&copy; 2024 SOFE Studio, SH32x.</p>
    </footer>
  </body>
</html>

```

# app\views.py

```py
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
```

# config.py

```py
# config.py

import os

class Config:
    """Configuration class for Flask application settings"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

# products.txt

```txt
1,Product A,10.99,Type 1,https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f
2,Product B,15.49,Type 2,https://images.unsplash.com/photo-1567306226416-28f0efdc88ce
3,Product C,8.99,Type 3,https://unsplash.com/photos/gold-and-silver-colored-pendant-necklace-TxCbfMc854c
stx3,test,3.59,food,https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.istockphoto.com%2Fphoto%2Fclose-up-of-a-fresh-yellow-pear-with-clipping-path-gm183387755-15702220&psig=AOvVaw1V0ZqxpD1MJVTTvK4PyUNG&ust=1729712454305000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCICeypTfookDFQAAAAAdAAAAABAE
```

# README.md

```md
# WebAPI
A Flask web application that displays data from a cloud-hosted DB using a CRUD API
URL: "https://webapi-439022.nn.r.appspot.com"
Service Account: "webapi-439022@appspot.gserviceaccount.com"
```

# requirements.txt

```txt
blinker==1.8.2
click==8.1.7
colorama==0.4.6
Flask==3.0.3
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
Werkzeug==3.0.4
mysqlclient==2.2.4
flask-sqlalchemy==3.1.1
flask-wtf==1.2.1
flask-bootstrap==3.3.7.1
PyJWT
PyMySQL
```

# runpoint.py

```py
# Application runpoint file

# runpoint.py
from app import app

if __name__ == '__main__':
    app.run(debug=True)



```

