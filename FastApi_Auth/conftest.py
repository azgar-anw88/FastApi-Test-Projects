import pytest
from fastapi.testclient import TestClient
from main import app
from auth import create_jwt_token

@pytest.fixture(scope='module')
def test_client():
    client = TestClient(app)
    yield client
 
def test_create_and_read_item(test_client):
    token = create_jwt_token(data={"sub":"azgar"})
    response = test_client.post("/items/", json={"name": "testuser", "email": "testuser@gmail.com"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    item_id = response.json()["id"]
    response = test_client.get(f"/items/{item_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["name"] == "testuser"
    assert response.json()["email"] == "testuser@gmail.com"

def test_read_items(test_client):
    token = create_jwt_token(data={"sub":"azgar"})
    test_client.post("/items/", json={"name": "testuser1", "email": "testuser1@gmail.com"}, headers={"Authorization": f"Bearer {token}"})
    test_client.post("/items/", json={"name": "testuser2", "email": "testuser2@gmail.com"}, headers={"Authorization": f"Bearer {token}"})
    response = test_client.get("/items/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0
    for item in items:
        assert "id" in item
        assert "name" in item
        assert "email" in item
        assert isinstance(item["id"], int)
        assert isinstance(item["name"], str)
        assert isinstance(item["email"], str)

def test_update_item(test_client):
    token = create_jwt_token(data={"sub":"azgar"})
    response = test_client.post("/items/", json={"name": "testitem", "email": "testitem@gmail.com"}, headers={"Authorization": f"Bearer {token}"})
    item_id = response.json()["id"]
    response = test_client.put(f"/items/{item_id}", json={"name": "updateduser", "email": "updateduser@gmail.com"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "updateduser"
    assert response.json()["email"] == "updateduser@gmail.com"

def test_delete_item(test_client):
    token = create_jwt_token(data={"sub":"azgar"})
    response = test_client.post("/items/", json={"name": "test_client", "email": "test@gmail.com"}, headers={"Authorization": f"Bearer {token}"})
    item_id = response.json()["id"]
    response = test_client.delete(f"/items/{item_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == item_id


