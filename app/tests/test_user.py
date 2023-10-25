from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.config.db import SessionLocal
from app.main import app

client = TestClient(app)

def test_create_user():
    with SessionLocal() as db:
        response = client.post("/users/", json={"username": "test_user", "password": "test_password"})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["username"] == "test_user"

def test_get_user():
    with SessionLocal() as db:
        user_create_response = client.post("/users/", json={"username": "test_user", "password": "test_password"})
        user_id = user_create_response.json()["id"]
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id

def test_get_users():
    with SessionLocal() as db:
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

def test_update_user():
    with SessionLocal() as db:
        user_create_response = client.post("/users/", json={"username": "test_user", "password": "test_password"})
        user_id = user_create_response.json()["id"]
        response = client.put(f"/users/{user_id}", json={"username": "updated_user", "password": "updated_password"})
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updated_user"

def test_delete_user():
    with SessionLocal() as db:
        user_create_response = client.post("/users/", json={"username": "test_user", "password": "test_password"})
        user_id = user_create_response.json()["id"]
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 200