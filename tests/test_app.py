import pytest
from app import app
from inventory_data import inventory


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_inventory():
    inventory.clear()
    inventory.append({
        "id": 1,
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 350,
        "stock": 20,
        "barcode": "123456789",
        "ingredients": "Filtered water, almonds, cane sugar",
        "categories": "Beverages",
        "image_url": "",
        "source": "mock"
    })


def test_home_route(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory Management API"


def test_get_all_inventory(client):
    response = client.get("/inventory")

    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_single_inventory_item(client):
    response = client.get("/inventory/1")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Organic Almond Milk"


def test_get_missing_inventory_item(client):
    response = client.get("/inventory/99")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Inventory item not found"


def test_add_inventory_item(client):
    new_item = {
        "name": "Chocolate Bar",
        "brand": "Cadbury",
        "price": 150,
        "stock": 30,
        "barcode": "987654321"
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 201
    assert response.get_json()["item"]["name"] == "Chocolate Bar"
    assert len(inventory) == 2


def test_add_inventory_item_missing_field(client):
    new_item = {
        "name": "Chocolate Bar",
        "brand": "Cadbury"
    }

    response = client.post("/inventory", json=new_item)

    assert response.status_code == 400


def test_update_inventory_item(client):
    response = client.patch("/inventory/1", json={
        "price": 400,
        "stock": 15
    })

    assert response.status_code == 200
    assert response.get_json()["item"]["price"] == 400
    assert response.get_json()["item"]["stock"] == 15


def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")

    assert response.status_code == 200
    assert len(inventory) == 0


def test_delete_missing_inventory_item(client):
    response = client.delete("/inventory/99")

    assert response.status_code == 404


def test_external_barcode_route(client, monkeypatch):
    def fake_fetch_product_by_barcode(barcode):
        return {
            "name": "Nutella",
            "brand": "Ferrero",
            "barcode": barcode,
            "ingredients": "Sugar, palm oil, hazelnuts",
            "categories": "Spreads",
            "image_url": "",
            "source": "OpenFoodFacts"
        }

    monkeypatch.setattr(
        "app.fetch_product_by_barcode",
        fake_fetch_product_by_barcode
    )

    response = client.get("/external/barcode/3017624010701")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Nutella"


def test_import_product_by_barcode(client, monkeypatch):
    def fake_fetch_product_by_barcode(barcode):
        return {
            "name": "Nutella",
            "brand": "Ferrero",
            "barcode": barcode,
            "ingredients": "Sugar, palm oil, hazelnuts",
            "categories": "Spreads",
            "image_url": "",
            "source": "OpenFoodFacts"
        }

    monkeypatch.setattr(
        "app.fetch_product_by_barcode",
        fake_fetch_product_by_barcode
    )

    response = client.post("/inventory/import/barcode/3017624010701", json={
        "price": 500,
        "stock": 10
    })

    assert response.status_code == 201
    assert response.get_json()["item"]["name"] == "Nutella"
    assert len(inventory) == 2