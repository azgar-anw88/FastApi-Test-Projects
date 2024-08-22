import pytest
from fastapi.testclient import TestClient
from basic_auth_api import app

client = TestClient(app)

@pytest.fixture
def get_client():
    return TestClient(app)

def test_valid_credentials():
    response = client.get("/basic-auth", auth=('testuser','testpass'))
    assert response.status_code == 200
    assert response.json() == {"message":"Authenticated Successfully"}

def test_invalid_credentials():
    response = client.get("/basic-auth", auth=('invaliduser','invalidpass'))
    assert response.status_code == 401
    assert response.json() == {"detail":"Invalid Credentials"}

def test_missing_credentials():
    response = client.get("/basic-auth")
    assert response.status_code == 401
    assert response.json() == {"detail":"Not authenticated"}

