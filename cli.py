import requests

BASE_URL = "http://127.0.0.1:5555"


def view_inventory():
    response = requests.get(f"{BASE_URL}/inventory")

    if response.status_code == 200:
        inventory = response.json()

        if not inventory:
            print("\nInventory is empty.\n")
            return

        print("\n========== INVENTORY ==========")

        for item in inventory:
            print(f"""
ID: {item['id']}
Name: {item['name']}
Brand: {item['brand']}
Price: KES {item['price']}
Stock: {item['stock']}
Barcode: {item['barcode']}
Source: {item['source']}
------------------------------
""")
    else:
        print("Failed to fetch inventory.")


def add_item():
    print("\nAdd Inventory Item")

    data = {
        "name": input("Name: "),
        "brand": input("Brand: "),
        "price": float(input("Price: ")),
        "stock": int(input("Stock: ")),
        "barcode": input("Barcode (optional): ")
    }

    response = requests.post(f"{BASE_URL}/inventory", json=data)

    print(response.json())


def update_item():
    item_id = input("Item ID: ")

    data = {}

    price = input("New Price (leave blank to skip): ")

    if price:
        data["price"] = float(price)

    stock = input("New Stock (leave blank to skip): ")

    if stock:
        data["stock"] = int(stock)

    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )

    print(response.json())


def delete_item():
    item_id = input("Item ID: ")

    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")

    print(response.json())


def search_barcode():
    barcode = input("Barcode: ")

    response = requests.get(
        f"{BASE_URL}/external/barcode/{barcode}"
    )

    print(response.json())


def import_barcode():
    barcode = input("Barcode: ")

    price = float(input("Selling Price: "))
    stock = int(input("Stock: "))

    response = requests.post(
        f"{BASE_URL}/inventory/import/barcode/{barcode}",
        json={
            "price": price,
            "stock": stock
        }
    )

    print(response.json())


def menu():
    while True:

        print("""
==============================
Inventory Management System
==============================

1. View Inventory
2. Add Item
3. Update Item
4. Delete Item
5. Search Product (OpenFoodFacts)
6. Import Product to Inventory
7. Exit
""")

        choice = input("Choose: ")

        if choice == "1":
            view_inventory()

        elif choice == "2":
            add_item()

        elif choice == "3":
            update_item()

        elif choice == "4":
            delete_item()

        elif choice == "5":
            search_barcode()

        elif choice == "6":
            import_barcode()

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()