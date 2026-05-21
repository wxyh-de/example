from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import threading

app = Flask(__name__)
CORS(app)

game_data = {
    "players": {},
    "current_player": None
}
data_lock = threading.Lock()

class Player:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp = 100
        self.exp = 0
        self.inventory = {}

    def fight(self):
        self.exp += 10
        self.hp = max(0, self.hp - 20)

    def get_status(self):
        return {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "exp": self.exp
        }

    def add_item(self, item_name, quantity=1):
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            self.inventory[item_name] = quantity

    def remove_item(self, item_name, quantity=1):
        if item_name in self.inventory:
            if self.inventory[item_name] >= quantity:
                self.inventory[item_name] -= quantity
                if self.inventory[item_name] == 0:
                    del self.inventory[item_name]
                return True
        return False

    def trade_item(self, other_player, item_name, quantity=1):
        if self.remove_item(item_name, quantity):
            other_player.add_item(item_name, quantity)
            return True
        return False

    def get_inventory(self):
        return self.inventory

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "hp": self.hp,
            "exp": self.exp,
            "inventory": self.inventory
        }

@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "MUD Game API is running"}), 200

@app.route("/api/player", methods=["POST"])
def create_player():
    try:
        data = request.get_json()
        if not data or "name" not in data:
            return jsonify({"success": False, "error": "Name is required"}), 400
        
        name = data["name"]
        if not name:
            return jsonify({"success": False, "error": "Name cannot be empty"}), 400
        
        player_id = str(uuid.uuid4())
        
        with data_lock:
            new_player = Player(name)
            game_data["players"][player_id] = new_player
            game_data["current_player"] = player_id
            
            return jsonify({
                "success": True,
                "player_id": player_id,
                "player": new_player.to_dict()
            }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/player/other", methods=["POST"])
def create_other_player():
    try:
        data = request.get_json()
        if not data or "name" not in data:
            return jsonify({"success": False, "error": "Name is required"}), 400
        
        name = data["name"]
        if not name:
            return jsonify({"success": False, "error": "Name cannot be empty"}), 400
        
        player_id = str(uuid.uuid4())
        
        with data_lock:
            new_player = Player(name)
            game_data["players"][player_id] = new_player
            
            return jsonify({
                "success": True,
                "player_id": player_id,
                "player": new_player.to_dict()
            }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/player", methods=["GET"])
def get_player():
    try:
        with data_lock:
            if not game_data["current_player"]:
                return jsonify({"success": False, "error": "No player selected"}), 404
            
            current_player_id = game_data["current_player"]
            player = game_data["players"].get(current_player_id)
            
            if not player:
                return jsonify({"success": False, "error": "Player not found"}), 404
            
            return jsonify({
                "success": True,
                "player": player.to_dict()
            }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/fight", methods=["POST"])
def fight():
    try:
        with data_lock:
            if not game_data["current_player"]:
                return jsonify({"success": False, "error": "No player selected"}), 404
            
            player_id = game_data["current_player"]
            player = game_data["players"].get(player_id)
            
            if not player:
                return jsonify({"success": False, "error": "Player not found"}), 404
            
            old_hp = player.hp
            old_exp = player.exp
            player.fight()
            
            return jsonify({
                "success": True,
                "player": player.to_dict(),
                "message": "Fight completed!",
                "exp_gained": 10,
                "hp_lost": old_hp - player.hp
            }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/inventory/item", methods=["POST"])
def add_item():
    try:
        data = request.get_json()
        if not data or "item_name" not in data:
            return jsonify({"success": False, "error": "Item name is required"}), 400
        
        item_name = data["item_name"]
        quantity = data.get("quantity", 1)
        
        if not isinstance(quantity, int) or quantity < 1:
            return jsonify({"success": False, "error": "Quantity must be positive integer"}), 400
        
        with data_lock:
            if not game_data["current_player"]:
                return jsonify({"success": False, "error": "No player selected"}), 404
            
            player_id = game_data["current_player"]
            player = game_data["players"].get(player_id)
            
            if not player:
                return jsonify({"success": False, "error": "Player not found"}), 404
            
            player.add_item(item_name, quantity)
            
            return jsonify({
                "success": True,
                "player": player.to_dict()
            }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    try:
        with data_lock:
            if not game_data["current_player"]:
                return jsonify({"success": False, "error": "No player selected"}), 404
            
            player_id = game_data["current_player"]
            player = game_data["players"].get(player_id)
            
            if not player:
                return jsonify({"success": False, "error": "Player not found"}), 404
            
            return jsonify({
                "success": True,
                "inventory": player.get_inventory()
            }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/trade", methods=["POST"])
def trade_item():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "Request body is required"}), 400
        
        item_name = data.get("item_name")
        quantity = data.get("quantity", 1)
        target_player_id = data.get("target_player_id")
        
        if not item_name:
            return jsonify({"success": False, "error": "Item name is required"}), 400
        
        if not target_player_id:
            return jsonify({"success": False, "error": "Target player ID is required"}), 400
        
        if not isinstance(quantity, int) or quantity < 1:
            return jsonify({"success": False, "error": "Quantity must be positive integer"}), 400
        
        with data_lock:
            if not game_data["current_player"]:
                return jsonify({"success": False, "error": "No player selected"}), 404
            
            source_player_id = game_data["current_player"]
            source_player = game_data["players"].get(source_player_id)
            target_player = game_data["players"].get(target_player_id)
            
            if not source_player:
                return jsonify({"success": False, "error": "Source player not found"}), 404
            
            if not target_player:
                return jsonify({"success": False, "error": "Target player not found"}), 404
            
            success = source_player.trade_item(target_player, item_name, quantity)
            
            if success:
                return jsonify({
                    "success": True,
                    "message": f"Traded {quantity} {item_name} successfully!",
                    "source_player": source_player.to_dict(),
                    "target_player": target_player.to_dict()
                }), 200
            else:
                return jsonify({"success": False, "error": "Trade failed. Not enough items in inventory"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/players", methods=["GET"])
def get_all_players():
    try:
        with data_lock:
            players_list = []
            for player_id, player in game_data["players"].items():
                players_list.append({
                    "player_id": player_id,
                    **player.to_dict()
                })
            
            return jsonify({
                "success": True,
                "players": players_list
            }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/game/reset", methods=["POST"])
def reset_game():
    try:
        with data_lock:
            game_data["players"] = {}
            game_data["current_player"] = None
            
            return jsonify({
                "success": True,
                "message": "Game has been reset"
            }), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)