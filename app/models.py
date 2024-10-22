# Handles users and authentication, contains classes to represent users
# Contains variables for each class, including id, passwords, credentials
# Potentially has additional classes for departments, roles, etc. 

import os

def load_products():
    """Load products from file"""
    products = []
    # Check if the file exists before trying to read it
    if os.path.exists('products.txt'):
        with open('products.txt', 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 5:
                    product = {
                        'id': parts[0],
                        'name': parts[1],
                        'price': parts[2],
                        'type': parts[3],
                        'image': parts[4]
                    }
                    products.append(product)
    return products

def save_product(product):
    """Save a new product to the file"""
    # Append a new product to the file with a newline
    with open('products.txt', 'a') as file:
        if os.path.getsize('products.txt') > 0:
            file.write("\n")
        file.write(f"{product['id']},{product['name']},{product['price']},{product['type']},{product['image']}")

