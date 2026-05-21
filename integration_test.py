import pytest
import requests
import json
import time

BASE_URL = "http://localhost:5000/api"

def test_health_check():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_create_player():
    test_name = "TestPlayer"
    response = requests.post(
        f"{BASE_URL}/player",
        json={"name": test_name},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["player"]["name"] == test_name
    assert data["player"]["hp"] == 100
    assert data["player"]["exp"] == 0
    return data["player_id"]

def test_fight():
    player_id = test_create_player()
    
    response = requests.post(f"{BASE_URL}/fight")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["player"]["exp"] == 10
    assert data["player"]["hp"] == 80

def test_add_item():
    test_create_player()
    
    response = requests.post(
        f"{BASE_URL}/inventory/item",
        json={"item_name": "Sword", "quantity": 2},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["player"]["inventory"]["Sword"] == 2

def test_get_inventory():
    test_add_item()
    
    response = requests.get(f"{BASE_URL}/inventory")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Sword" in data["inventory"]

def test_trade_item():
    player_id = test_create_player()
    
    other_response = requests.post(
        f"{BASE_URL}/player/other",
        json={"name": "OtherPlayer"},
        headers={"Content-Type": "application/json"}
    )
    assert other_response.status_code == 201
    other_player_id = other_response.json()["player_id"]
    
    requests.post(
        f"{BASE_URL}/inventory/item",
        json={"item_name": "Sword", "quantity": 2},
        headers={"Content-Type": "application/json"}
    )
    
    trade_response = requests.post(
        f"{BASE_URL}/trade",
        json={
            "item_name": "Sword",
            "quantity": 1,
            "target_player_id": other_player_id
        },
        headers={"Content-Type": "application/json"}
    )
    assert trade_response.status_code == 200
    trade_data = trade_response.json()
    assert trade_data["success"] is True
    assert trade_data["source_player"]["inventory"]["Sword"] == 1
    assert trade_data["target_player"]["inventory"]["Sword"] == 1

def test_get_all_players():
    test_create_player()
    
    response = requests.get(f"{BASE_URL}/players")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["players"], list)
    assert len(data["players"]) > 0

def test_reset_game():
    test_create_player()
    
    response = requests.post(f"{BASE_URL}/game/reset")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    get_response = requests.get(f"{BASE_URL}/players")
    get_data = get_response.json()
    assert len(get_data["players"]) == 0

if __name__ == "__main__":
    test_health_check()
    print("✓ Health check passed")
    
    test_create_player()
    print("✓ Create player passed")
    
    test_fight()
    print("✓ Fight passed")
    
    test_add_item()
    print("✓ Add item passed")
    
    test_get_inventory()
    print("✓ Get inventory passed")
    
    test_trade_item()
    print("✓ Trade item passed")
    
    test_get_all_players()
    print("✓ Get all players passed")
    
    test_reset_game()
    print("✓ Reset game passed")
    
    print("\n🎉 All API integration tests passed!")