from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.config.db import SessionLocal
from main import app

client = TestClient(app)


def test_create_deck():
    with SessionLocal() as db:
        response = client.post("/decks/", json={"name": "Test Deck"})
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Deck"


def test_get_deck():
    with SessionLocal() as db:
        deck_create_response = client.post(
            "/decks/", json={"name": "Test Deck"})
        deck_id = deck_create_response.json()["id"]
        response = client.get(f"/decks/{deck_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == deck_id


def test_get_decks():
    with SessionLocal() as db:
        response = client.get("/decks/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


def test_update_deck():
    with SessionLocal() as db:
        deck_create_response = client.post(
            "/decks/", json={"name": "Test Deck"})
        deck_id = deck_create_response.json()["id"]
        response = client.put(
            f"/decks/{deck_id}", json={"name": "Updated Deck"})
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Deck"


def test_delete_deck():
    with SessionLocal() as db:
        deck_create_response = client.post(
            "/decks/", json={"name": "Test Deck"})
        deck_id = deck_create_response.json()["id"]
        response = client.delete(f"/decks/{deck_id}")
        assert response.status_code == 200


def test_add_card_to_deck():
    with SessionLocal() as db:
        deck_create_response = client.post(
            "/decks/", json={"name": "Test Deck"})
        deck_id = deck_create_response.json()["id"]
        card_create_response = client.post(
            "/cards/", json={"name": "Test Card"})
        card_id = card_create_response.json()["id"]
        response = client.post(f"/decks/{deck_id}/cards/{card_id}")
        assert response.status_code == 200


def test_remove_card_from_deck():
    with SessionLocal() as db:
        deck_create_response = client.post(
            "/decks/", json={"name": "Test Deck"})
        deck_id = deck_create_response.json()["id"]
        card_create_response = client.post(
            "/cards/", json={"name": "Test Card"})
        card_id = card_create_response.json()["id"]
        add_card_response = client.post(f"/decks/{deck_id}/cards/{card_id}")
        response = client.delete(f"/decks/{deck_id}/cards/{card_id}")
        assert response.status_code == 200
