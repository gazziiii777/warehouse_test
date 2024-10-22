from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_product():
    product_data = {
        "title": "Продукт_тест_",
        "description": "Продукт_тест_",
        "price": 20.01,
        "stock": 100
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == product_data["title"]
    assert response_data["description"] == product_data["description"]
    assert response_data["price"] == product_data["price"]
    assert response_data["stock"] == product_data["stock"]


def test_create_product_missing_fields():
    product_data = {
        "title": "Test Product"
    }

    response = client.post("/products/", json=product_data)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_get_products():
    response = client.get("/products/")

    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
