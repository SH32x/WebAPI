# CRUD API Documentation

## URL
`https://webapi-439022.nn.r.appspot.com`

## Authentication
All API endpoints except the login require Admin token authentication, which is granted by successful login. 

## API Overview

| Endpoint | Method | Description | Request Format | Success Response | Error Response(s) |
|----------|---------|-------------|----------------|------------------|----------------|
| `/auth/login` | POST | Get authentication token | username, password | Auth Token | `"Invalid credentials"` if either input is incorrect, `"Missing required fields"` if either input is missing |
| `/products` | GET | Get all products | None | Displays all items | SQL Error 200: `"Rejected"` |
| `/products/<product_id>` | GET | Get single product | None | Displays one item | SQL Errors 200, 404 |
| `/products` | POST | Create new product | Form with "id", "name", "price", "type", "image" | `"Product created successfully"` | `"Missing required fields"` if any field missing, `"No data provided"` if all fields empty |
| `/products/<product_id>` | PUT | Update product | Form with "name", "price", "type", "image" | `"Product updated successfully"` | `"No update data provided"` if all fields empty |
| `/products/<product_id>` | DELETE | Delete product | None | `"Product deleted successfully"` | SQL Error 404 |
