from flask import Flask, jsonify, request
from flask_cors import CORS
from inventory_data import inventory

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
            "DELETE /inventory/<id>"
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

    allowed_fields = ["name", "brand", "price", "stock", "barcode", "ingredients"]

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


if __name__ == "__main__":
    app.run(debug=True, port=5555)