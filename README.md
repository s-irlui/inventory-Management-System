# Inventory Management System API

## Project Description

This is a Flask-based REST API for managing inventory items for a small retail company. The system allows employees to add, view, update, and delete inventory products. It also integrates with the OpenFoodFacts API to fetch product details using a barcode.

## Features

- View all inventory items
- View a single inventory item
- Add new inventory items
- Update item price or stock
- Delete inventory items
- Fetch product details from OpenFoodFacts API
- Import external product data into inventory
- CLI interface for interacting with the API
- Pytest test suite

## Technologies Used

- Python
- Flask
- Flask-CORS
- Requests
- Pytest
- OpenFoodFacts API
- Git and GitHub

## API Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | API home route |
| GET | `/inventory` | Fetch all inventory items |
| GET | `/inventory/<id>` | Fetch one inventory item |
| POST | `/inventory` | Add a new inventory item |
| PATCH | `/inventory/<id>` | Update an inventory item |
| DELETE | `/inventory/<id>` | Delete an inventory item |
| GET | `/external/barcode/<barcode>` | Fetch product from OpenFoodFacts by barcode |
| GET | `/external/search/<name>` | Search product from OpenFoodFacts by name |
| POST | `/inventory/import/barcode/<barcode>` | Import product from OpenFoodFacts into inventory |

## Installation

```bash
git clone git@github.com:s-irlui/inventory-Management-System.git
cd inventory-Management-System
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

