# CodeAlpha_EcommerceStore (ShopEase)

A simple e-commerce store built with **Django** for the CodeAlpha Full Stack Development Internship (Task 1).

## Features
- Product listing with categories and search
- Product details page
- Shopping cart (session based: add, update quantity, remove)
- User registration, login and logout
- Checkout and order processing (stock is reduced when an order is placed)
- Order history and order details for each user
- Django admin to manage products, categories and orders
- SQLite database storing products, users and orders

## Tech stack
HTML, CSS, JavaScript, Python 3, Django 5.2, SQLite

## Run locally (Windows)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_products
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ for the store and http://127.0.0.1:8000/admin/ for the admin panel.

## Run tests
```bash
python manage.py test
```

## Project structure
| App | Purpose |
|-----|---------|
| `products` | Category and Product models, list/detail views, `seed_products` command |
| `cart` | Session-based Cart class and views |
| `orders` | Order and OrderItem models, checkout, order history |
| `accounts` | Registration, login, logout |
