# Django E-commerce Backend Documentation

This document provides a comprehensive overview of the backend architecture, setup instructions, and detailed API reference with payloads.

## 1. Project Reference

- **Base URL**: `http://localhost:8000` (Local)
- **Auth Header**: `Authorization: Bearer <access_token>`

## 2. API Endpoints & Payloads

### Authentication

`POST` `/api/users/login/`

- **Description**: Authenticate user and get tokens.
- **Request (JSON)**:
  ```json
  {
    "email": "user@example.com", // String (Required)
    "password": "password123" // String (Required)
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "id": 1,
    "_id": 1,
    "username": "user@example.com",
    "email": "user@example.com",
    "name": "John Doe",
    "isAdmin": false,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." // Access Token
  }
  ```

`POST` `/api/users/register/`

- **Description**: Register a new user.
- **Request (JSON)**:
  ```json
  {
    "name": "John Doe", // String (Required)
    "email": "new@example.com", // String (Required)
    "password": "strongPassword" // String (Required)
  }
  ```
- **Response (200 OK)**: Same structure as Login response.

`GET` `/api/users/profile/`

- **Auth**: Required
- **Response (200 OK)**:
  ```json
  {
    "id": 1,
    "_id": 1,
    "username": "user@example.com",
    "email": "user@example.com",
    "name": "John Doe",
    "isAdmin": false
  }
  ```

### Products

`GET` `/api/products/`

- **Query Params**: `?keyword=iphone&page=1`
- **Response (200 OK)**:
  ```json
  {
    "products": [
      {
        "id": 1,
        "user": 1,
        "name": "iPhone 13",
        "image": "/images/sample.jpg",
        "brand": "Apple",
        "category": "Electronics",
        "description": "Phone description",
        "rating": "4.50",
        "numReviews": 10,
        "price": "999.99",
        "countInStock": 5,
        "createdAt": "2023-01-01T12:00:00Z",
        "reviews": []
      }
    ],
    "page": 1,
    "pages": 10
  }
  ```

`POST` `/api/products/create/`

- **Auth**: Admin Required
- **Request**: Empty Body (Creates sample product)
- **Response (200 OK)**: Returns the created sample product object.

`PUT` `/api/products/update/<id>/`

- **Auth**: Admin Required
- **Request (JSON)**:
  ```json
  {
    "name": "New Name", // String
    "price": 1099.99, // Decimal/Float
    "brand": "Apple", // String
    "countInStock": 10, // Integer
    "category": "Electronics", // String
    "description": "Updated..." // String
  }
  ```

`POST` `/api/products/<id>/reviews/`

- **Auth**: Required
- **Request (JSON)**:
  ```json
  {
    "rating": 5, // Integer (1-5)
    "comment": "Great product!" // String
  }
  ```
- **Response (200 OK)**: `"Review Added"`

### Orders

`POST` `/api/orders/add/`

- **Auth**: Required
- **Request (JSON)**:
  ```json
  {
    "orderItems": [
      {
        "product": 1, // Integer (Product ID)
        "name": "iPhone 13", // String
        "qty": 1, // Integer
        "price": 999.99, // Decimal
        "image": "/images/..." // String
      }
    ],
    "shippingAddress": {
      "address": "123 Main St", // String
      "city": "New York", // String
      "postalCode": "10001", // String
      "country": "USA" // String
    },
    "paymentMethod": "PayPal", // String
    "itemsPrice": 999.99, // Decimal
    "taxPrice": 50.0, // Decimal
    "shippingPrice": 10.0, // Decimal
    "totalPrice": 1059.99 // Decimal
  }
  ```
- **Response (200 OK)**: Full Order object including `_id` and status.

`GET` `/api/orders/<id>/`

- **Auth**: Required (Owner or Admin)
- **Response (200 OK)**:
  ```json
  {
    "_id": 1,
    "user": { "id": 1, "name": "John", "email": "..." },
    "orderItems": [ ... ],
    "shippingAddress": { ... },
    "paymentMethod": "PayPal",
    "taxPrice": "50.00",
    "isPaid": false,
    "isDelivered": false,
    ...
  }
  ```

`PUT` `/api/orders/<id>/pay/`

- **Auth**: Required
- **Description**: Mark order as paid (usually called by payment gateway callback).
- **Response**: `"Order was paid"`

`PUT` `/api/orders/<id>/deliver/`

- **Auth**: Admin Required
- **Response**: `"Order was delivered"`

## 3. Setup & Running

- **Run Tests**: `python manage.py test base`
- **Run Server**: `python manage.py runserver`
- **Docker**: `docker-compose up --build`
