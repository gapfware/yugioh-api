from fastapi.testclient import TestClient
from app.main import app  # Asegúrate de importar tu aplicación FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.schemas.card import CardBase
from app.config.db import URL, Base


# Configura una base de datos temporal para las pruebas
engine = create_engine(URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Crea un cliente de prueba
client = TestClient(app)

def test_create_card():
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
    assert created_card["name"] == card_data["name"]


    # Create a card to update
    card_data = {
        "name": "Test Card",
        "type": "Monster",
        "attack": 1000,
        "defense": 800,
        "description": "A test card.",
        "image_url": "https://example.com/test.jpg"
    }
    response = client.post("/cards/", json=card_data)
    assert response.status_code == 200
    created_card = response.json()

    # Update the card
    updated_card_data = {
        "name": "Updated Test Card",
        "type": "Spell",
        "attack": None,
        "defense": None,
        "description": "An updated test card.",
        "image_url": "https://example.com/updated_test.jpg"
    }
    response = client.put(f"/cards/{created_card['id']}", json=updated_card_data)
    assert response.status_code == 200
    updated_card = response.json()
    assert updated_card["name"] == updated_card_data["name"]
    assert updated_card["type"] == updated_card_data["type"]
    assert updated_card["attack"] == updated_card_data["attack"]
    assert updated_card["defense"] == updated_card_data["defense"]
    assert updated_card["description"] == updated_card_data["description"]
    assert updated_card["image_url"] == updated_card_data["image_url"]
    
def test_update_card_invalid_id():
    # Try to update a card with an invalid ID
    updated_card_data = {
        "name": "Updated Test Card",
        "type": "Spell",
        "attack": None,
        "defense": None,
        "description": "An updated test card.",
        "image_url": "https://example.com/updated_test.jpg"
    }
    response = client.put("/cards/999", json=updated_card_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"
    
def test_update_card_invalid_data():
    # Create a card to update
    card_data = {
        "name": "Test jjjjj",
        "type": "Monster",
        "attack": 1000,
        "defense": 800,
        "description": "A test card.",
        "image_url": "https://example.com/test.jpg"
    }
    response = client.post("/cards/", json=card_data)
    assert response.status_code == 200
    created_card = response.json()

    # Try to update the card with invalid data
    updated_card_data = {
        "name": "",
        "type": "Invalid",
        "attack": "not a number",
        "defense": "not a number",
        "description": "",
        "image_url": "not a URL"
    }
    response = client.put(f"/cards/{created_card['id']}", json=updated_card_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "field required"
    assert response.json()["detail"][1]["msg"] == "value is not a valid enumeration member; permitted: 'Monster', 'Spell', 'Trap'"
    assert response.json()["detail"][2]["msg"] == "value is not a valid integer"
    assert response.json()["detail"][3]["msg"] == "value is not a valid integer"
    assert response.json()["detail"][4]["msg"] == "ensure this value has at least 1 characters"
    assert response.json()["detail"][5]["msg"] == "value is not a valid URL"