import unittest

from fastapi.testclient import TestClient

from src.app import app
from src.models import Item

client = TestClient(app)


class TestStringMethods(unittest.TestCase):
    def test_create_items(self):
        items = [
            Item(id=1, name="Laptop", price=999.99, is_offer=True),
            Item(id=2, name="Smartphone", price=599.99, is_offer=False),
            Item(id=3, name="Headphones", price=199.99, is_offer=True),
            Item(id=4, name="Monitor", price=299.99, is_offer=False),
            Item(id=5, name="Keyboard", price=49.99, is_offer=True),
            Item(id=6, name="Mouse", price=29.99, is_offer=False),
            Item(id=7, name="Printer", price=149.99, is_offer=True),
            Item(id=8, name="Webcam", price=89.99, is_offer=False),
            Item(id=9, name="External Hard Drive", price=79.99, is_offer=True),
            Item(id=10, name="USB Flash Drive", price=19.99, is_offer=False),
            # Item(id=1, name="Laptop", price=999.99, is_offer=True)
        ]

        for item in items:
            response = client.post("/items/", json=item.model_dump())
            assert response.status_code == 200
            data = response.json()
            assert data["name"] == item.name
            assert data["price"] == item.price
            assert data["is_offer"] == item.is_offer
            assert "id" in data


if __name__ == "__main__":
    unittest.main()
