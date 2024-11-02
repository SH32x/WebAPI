# CRUD API Documentation

## URL
`https://webapi-439022.nn.r.appspot.com`

## Authentication
All API endpoints except the login require Admin token authentication, which is granted by successful login. 

## API Overview

| Endpoint | Method | Description | Request Format | Success Response | Error Response |
|----------|---------|-------------|----------------|------------------|----------------|
| `/auth/login` | POST | Get authentication token | username, password | Auth Token | `"Invalid credentials"` |
| `/products` | GET | Get all products | None | Displays all items | `"Missing Token!"` |
| `/products/<product_id>` | GET | Get single product | None | Displays one item | `"Product not found"` |
| `/products` | POST | Create new product | Form with "id", "name", "price", "type", "image" | `"Product created successfully"` | `"Missing required fields"` |
| `/products/<product_id>` | PUT | Update product | Form with "name", "price", "type", "image" | `"Product updated successfully"` | `"Product not found"` |
| `/products/<product_id>` | DELETE | Delete product | None | `"Product deleted successfully"` | `"Product not found"` |
