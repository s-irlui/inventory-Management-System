from flask import Flask, jsonify, request
from flask_cors import CORS
from inventory_data import inventory
from openfoodfacts import fetch_product_by_barcode, search_product_by_name

app = Flask(__name__)
CORS(app)


def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


def generate_id():
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API",
        "routes": [
            "GET /inventory",
            "GET /inventory/<id>",
            "POST /inventory",
            "PATCH /inventory/<id>",
            "DELETE /inventory/<id>",
            "GET /external/barcode/<barcode>",
            "GET /external/search/<name>",
            "POST /inventory/import/barcode/<barcode>"
        ]
    })


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Inventory item not found"}), 404

    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def add_inventory_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    required_fields = ["name", "brand", "price", "stock"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    new_item = {
        "id": generate_id(),
        "name": data["name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"],
        "barcode": data.get("barcode", ""),
        "ingredients": data.get("ingredients", ""),
        "categories": data.get("categories", ""),
        "image_url": data.get("image_url", ""),
        "source": data.get("source", "manual")
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Inventory item added successfully",
        "item": new_item
    }), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Inventory item not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    allowed_fields = [
        "name",
        "brand",
        "price",
        "stock",
        "barcode",
        "ingredients",
        "categories",
        "image_url",
        "source"
    ]

    for key, value in data.items():
        if key in allowed_fields:
            item[key] = value

    return jsonify({
        "message": "Inventory item updated successfully",
        "item": item
    }), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Inventory item not found"}), 404

    inventory.remove(item)

    return jsonify({
        "message": "Inventory item deleted successfully"
    }), 200


@app.route("/external/barcode/<barcode>", methods=["GET"])
def external_product_by_barcode(barcode):
    product = fetch_product_by_barcode(barcode)

    if not product:
        return jsonify({"error": "Product not found from external API"}), 404

    return jsonify(product), 200


@app.route("/external/search/<name>", methods=["GET"])
def external_product_by_name(name):
    product = search_product_by_name(name)

    if not product:
        return jsonify({"error": "Product not found from external API"}), 404

    return jsonify(product), 200


@app.route("/inventory/import/barcode/<barcode>", methods=["POST"])
def import_product_by_barcode(barcode):
    product = fetch_product_by_barcode(barcode)

    if not product:
        return jsonify({"error": "Product not found from external API"}), 404

    data = request.get_json() if request.is_json else {}

    new_item = {
        "id": generate_id(),
        "name": product["name"],
        "brand": product["brand"],
        "price": data.get("price", 0),
        "stock": data.get("stock", 0),
        "barcode": product["barcode"],
        "ingredients": product["ingredients"],
        "categories": product["categories"],
        "image_url": product["image_url"],
        "source": product["source"]
    }

    inventory.append(new_item)

    return jsonify({
        "message": "Product imported and added to inventory successfully",
        "item": new_item
    }), 201


if __name__ == "__main__":
    app.run(debug=True, port=5555)