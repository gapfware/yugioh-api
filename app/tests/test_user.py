from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de importar tu aplicación FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.card import CardBase
from app.config.db import URL, Base


# Configura una base de datos temporal para las pruebas
engine = create_engine(URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_get_cards():
    # Create some test cards
    card_data = [
        {
            "name": "Test Card 1",
            "type": "Monster",
            "attack": 1000,
            "defense": 800,
            "description": "A test card.",
            "image_url": "https://example.com/test1.jpg"
        },
        {
            "name": "Test Card 2",
            "type": "Spell",
            "attack": None,
            "defense": None,
            "description": "Another test card.",
            "image_url": "https://example.com/test2.jpg"
        },
        {
            "name": "Test Card 3",
            "type": "Trap",
            "attack": None,
            "defense": None,
            "description": "Yet another test card.",
            "image_url": "https://example.com/test3.jpg"
        }
    ]
    for card in card_data:
        response = client.post("/cards/", json=card)
        assert response.status_code == 201

    # Retrieve the cards
    response = client.get("/cards/")
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) == len(card_data)
    for i, card in enumerate(cards):
        assert card["name"] == card_data[i]["name"]
        assert card["type"] == card_data[i]["type"]
        assert card["attack"] == card_data[i]["attack"]
        assert card["defense"] == card_data[i]["defense"]
        assert card["description"] == card_data[i]["description"]
        assert card["image_url"] == card_data[i]["image_url"]


def test_get_card():
    # Create a test card
    card_data = {
        "name": "Test Card",
        "type": "Monster",
        "attack": 1000,
        "defense": 800,
        "description": "A test card.",
        "image_url": "https://example.com/test.jpg"
    }
    response = client.post("/cards/", json=card_data)
    assert response.status_code == 201
    created_card = response.json()

    # Retrieve the card
    response = client.get(f"/cards/{created_card['id']}")
    assert response.status_code == 200
    card = response.json()
    assert card["name"] == card_data["name"]
    assert card["type"] == card_data["type"]
    assert card["attack"] == card_data["attack"]
    assert card["defense"] == card_data["defense"]
    assert card["description"] == card_data["description"]
    assert card["image_url"] == card_data["image_url"]


def test_delete_card():
    # Create a test card
    card_data = {
        "name": "Test Card",
        "type": "Monster",
        "attack": 1000,
        "defense": 800,
        "description": "A test card.",
        "image_url": "https://example.com/test.jpg"
    }
    response = client.post("/cards/", json=card_data)
    assert response.status_code == 201
    created_card = response.json()

    # Delete the card
    response = client.delete(f"/cards/{created_card['id']}")
    assert response.status_code == 200

    # Try to retrieve the card again
    response = client.get(f"/cards/{created_card['id']}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"
