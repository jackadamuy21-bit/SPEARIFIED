#!/usr/bin/env python3
"""
Spearified - Simple Python Version (No npm required!)
A multiplayer tag game with different modes.
"""

import asyncio
import json
import websockets
import random
import time
from collections import defaultdict

class GameServer:
    def __init__(self):
        self.players = {}  # player_id -> player_data
        self.game_mode = 'tag'  # tag, zombie, bomb
        self.tagger = None
        self.bomb_holder = None
        self.bomb_timer = 0
        self.map_size = 100  # -100 to +100
        self.obstacles = self.generate_obstacles()
        self.accounts = {}  # username -> password (simple storage)

    def generate_obstacles(self):
        """Generate obstacles based on current map"""
        map_configs = {
            'forest': {
                'name': 'Mystic Forest',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'tree', 'size': 8},
                    {'x': 20, 'z': 15, 'type': 'tree', 'size': 6},
                    {'x': -25, 'z': 10, 'type': 'tree', 'size': 7},
                    {'x': 15, 'z': -20, 'type': 'tree', 'size': 9},
                    {'x': -10, 'z': -15, 'type': 'tree', 'size': 5},
                    {'x': 30, 'z': 5, 'type': 'tree', 'size': 6},
                    {'x': -5, 'z': 25, 'type': 'tree', 'size': 8},
                    {'x': 25, 'z': -10, 'type': 'tree', 'size': 7},
                ]
            },
            'city': {
                'name': 'Urban Maze',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'building', 'size': 12},
                    {'x': 25, 'z': 0, 'type': 'building', 'size': 10},
                    {'x': -25, 'z': 0, 'type': 'building', 'size': 8},
                    {'x': 0, 'z': 25, 'type': 'building', 'size': 9},
                    {'x': 0, 'z': -25, 'type': 'building', 'size': 11},
                    {'x': 20, 'z': 20, 'type': 'building', 'size': 7},
                    {'x': -20, 'z': 20, 'type': 'building', 'size': 6},
                    {'x': 20, 'z': -20, 'type': 'building', 'size': 8},
                    {'x': -20, 'z': -20, 'type': 'building', 'size': 9},
                ]
            },
            'desert': {
                'name': 'Sandy Dunes',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'dune', 'size': 15},
                    {'x': 30, 'z': 10, 'type': 'dune', 'size': 12},
                    {'x': -30, 'z': -10, 'type': 'dune', 'size': 14},
                    {'x': 15, 'z': -25, 'type': 'cactus', 'size': 3},
                    {'x': -15, 'z': 25, 'type': 'cactus', 'size': 4},
                    {'x': 35, 'z': -5, 'type': 'cactus', 'size': 3},
                ]
            },
            'mountain': {
                'name': 'Mountain Peak',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'mountain', 'size': 20},
                    {'x': 25, 'z': 15, 'type': 'rock', 'size': 8},
                    {'x': -25, 'z': -15, 'type': 'rock', 'size': 10},
                    {'x': 15, 'z': -10, 'type': 'rock', 'size': 6},
                    {'x': -15, 'z': 10, 'type': 'rock', 'size': 7},
                ]
            },
            'beach': {
                'name': 'Tropical Beach',
                'obstacles': [
                    {'x': 0, 'z': 30, 'type': 'palm', 'size': 5},
                    {'x': 20, 'z': 25, 'type': 'palm', 'size': 6},
                    {'x': -20, 'z': 25, 'type': 'palm', 'size': 4},
                    {'x': 35, 'z': 20, 'type': 'palm', 'size': 5},
                    {'x': -35, 'z': 20, 'type': 'palm', 'size': 6},
                    {'x': 0, 'z': -30, 'type': 'rocks', 'size': 12},
                ]
            },
            'space': {
                'name': 'Space Station',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'station', 'size': 18},
                    {'x': 25, 'z': 0, 'type': 'satellite', 'size': 5},
                    {'x': -25, 'z': 0, 'type': 'satellite', 'size': 5},
                    {'x': 0, 'z': 25, 'type': 'satellite', 'size': 4},
                    {'x': 0, 'z': -25, 'type': 'satellite', 'size': 4},
                ]
            },
            'underwater': {
                'name': 'Deep Sea',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'coral', 'size': 10},
                    {'x': 20, 'z': 15, 'type': 'coral', 'size': 8},
                    {'x': -20, 'z': -15, 'type': 'coral', 'size': 9},
                    {'x': 15, 'z': -10, 'type': 'shipwreck', 'size': 12},
                    {'x': -15, 'z': 10, 'type': 'shipwreck', 'size': 10},
                ]
            },
            'castle': {
                'name': 'Medieval Castle',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'castle', 'size': 25},
                    {'x': 20, 'z': 0, 'type': 'tower', 'size': 8},
                    {'x': -20, 'z': 0, 'type': 'tower', 'size': 8},
                    {'x': 0, 'z': 20, 'type': 'tower', 'size': 7},
                    {'x': 0, 'z': -20, 'type': 'tower', 'size': 7},
                    {'x': 15, 'z': 15, 'type': 'wall', 'size': 6},
                    {'x': -15, 'z': -15, 'type': 'wall', 'size': 6},
                ]
            },
            'volcano': {
                'name': 'Volcanic Island',
                'obstacles': [
                    {'x': 0, 'z': 0, 'type': 'volcano', 'size': 22},
                    {'x': 20, 'z': 10, 'type': 'lava', 'size': 8},
                    {'x': -20, 'z': -10, 'type': 'lava', 'size': 9},
                    {'x': 15, 'z': -15, 'type': 'rock', 'size': 7},
                    {'x': -15, 'z': 15, 'type': 'rock', 'size': 6},
                ]
            }
        }

        # Randomly select a map
        map_names = list(map_configs.keys())
        selected_map = random.choice(map_names)
        self.current_map = map_configs[selected_map]
        
        return self.current_map['obstacles']

    def register_account(self, username, password):
        if username in self.accounts:
            return False, "Username already exists"
        self.accounts[username] = password
        return True, "Account created successfully"

    def login_account(self, username, password):
        if username not in self.accounts:
            return False, "Account not found"
        if self.accounts[username] != password:
            return False, "Incorrect password"
        return True, "Login successful"

    def add_player(self, player_id, username):
        if player_id in self.players:
            return False

        self.players[player_id] = {
            'id': player_id,
            'username': username,
            'x': random.uniform(-50, 50),
            'y': 1,
            'z': random.uniform(-50, 50),
            'is_tagger': False,
            'is_zombie': False,
            'is_alive': True,
            'kills': 0,
            'deaths': 0
        }

        # Set first player as tagger/zombie
        if len(self.players) == 1:
            if self.game_mode == 'tag':
                self.tagger = player_id
                self.players[player_id]['is_tagger'] = True
            elif self.game_mode == 'zombie':
                self.players[player_id]['is_zombie'] = True

        return True

    def remove_player(self, player_id):
        if player_id in self.players:
            del self.players[player_id]
            if self.tagger == player_id and self.players:
                self.tagger = next(iter(self.players.keys()))
                self.players[self.tagger]['is_tagger'] = True

    def get_game_state(self):
        return {
            'players': list(self.players.values()),
            'game_mode': self.game_mode,
            'tagger': self.tagger,
            'bomb_holder': self.bomb_holder,
            'bomb_timer': self.bomb_timer,
            'map_size': self.map_size,
            'obstacles': self.obstacles,
            'current_map': self.current_map
        }

# Global game server
game_server = GameServer()
connected_clients = {}

async def handle_client(websocket):
    player_id = None
    try:
        async for message in websocket:
            data = json.loads(message)

            if data['type'] == 'register':
                success, message = game_server.register_account(data['username'], data['password'])
                await websocket.send(json.dumps({
                    'type': 'auth_response',
                    'success': success,
                    'message': message
                }))

            elif data['type'] == 'login':
                success, message = game_server.login_account(data['username'], data['password'])
                if success:
                    player_id = 'player_' + str(hash(data['username']))[:8]
                    game_server.add_player(player_id, data['username'])
                    connected_clients[player_id] = websocket
                    await websocket.send(json.dumps({
                        'type': 'auth_response',
                        'success': True,
                        'message': message,
                        'player_id': player_id
                    }))
                    await broadcast_game_state()
                else:
                    await websocket.send(json.dumps({
                        'type': 'auth_response',
                        'success': False,
                        'message': message
                    }))

            elif data['type'] == 'join':
                player_id = data['player_id']
                username = data['username']
                game_server.add_player(player_id, username)
                connected_clients[player_id] = websocket

                # Send current game state
                await websocket.send(json.dumps({
                    'type': 'game_state',
                    'data': game_server.get_game_state()
                }))

                # Broadcast to all players
                await broadcast_game_state()

            elif data['type'] == 'move':
                if player_id and player_id in game_server.players:
                    game_server.players[player_id].update({
                        'x': data['x'],
                        'y': data['y'],
                        'z': data['z']
                    })
                    await broadcast_game_state()

            elif data['type'] == 'chat':
                if player_id:
                    message_data = {
                        'type': 'chat',
                        'username': game_server.players[player_id]['username'],
                        'message': data['message']
                    }
                    await broadcast(message_data)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if player_id:
            game_server.remove_player(player_id)
            if player_id in connected_clients:
                del connected_clients[player_id]
            await broadcast_game_state()

async def broadcast(data):
    message = json.dumps(data)
    for ws in connected_clients.values():
        try:
            await ws.send(message)
        except:
            pass

async def broadcast_game_state():
    state = game_server.get_game_state()
    await broadcast({
        'type': 'game_state',
        'data': state
    })

async def main():
    server = await websockets.serve(handle_client, "localhost", 8765)
    print("🎮 Spearified Server running on ws://localhost:8765")
    print("No npm required! Just run this Python script.")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())