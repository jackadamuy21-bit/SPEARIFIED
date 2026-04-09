# Spearified - Desktop App Edition!

This is now a **real desktop application** using Python and Pygame! No more web browsers - it's a proper game app.

## Features
- ✅ **Real Desktop App** - Native windowed game
- ✅ **9 Random Maps** - Forest, City, Desert, Mountain, Beach, Space, Underwater, Castle, Volcano
- ✅ **Multiple Game Modes** - Tag, Zombie, Hot Potato
- ✅ **Account System** - Login/Register with persistent accounts
- ✅ **Smooth Graphics** - Pygame-powered visuals
- ✅ **Real-time Multiplayer** - WebSocket connections
- ✅ **Camera System** - Follows your player
- ✅ **Obstacle Maps** - Different environments each game

## How to Run

### Step 1: Install Dependencies
**Option A (Automatic):**
- Double-click `run_desktop_game.bat` (installs everything automatically)

**Option B (Manual):**
```bash
pip install pygame websockets
python desktop_game.py
```

### Step 2: Start Server
In another terminal/command prompt:
```bash
python server.py
```

### Step 3: Play!
- **Login/Register** - Create an account or login
- **Quick Play** - Jump in as a guest
- **WASD** - Move around
- **Mouse** - Look around the map
- **ESC** - Return to menu

## Game Modes
- **Tag**: Classic tag - one person is "it"
- **Zombie**: Get tagged, become a zombie and infect others
- **Hot Potato**: Pass the bomb before it explodes!

## Maps
Each game randomly selects one of 9 unique maps:
1. **Mystic Forest** - Trees and nature
2. **Urban Maze** - City buildings
3. **Sandy Dunes** - Desert landscape
4. **Mountain Peak** - Rocky terrain
5. **Tropical Beach** - Palm trees and rocks
6. **Space Station** - Sci-fi environment
7. **Deep Sea** - Underwater coral
8. **Medieval Castle** - Castle and towers
9. **Volcanic Island** - Lava and rocks

## Controls
- **WASD** - Move
- **Mouse** - Camera control
- **ESC** - Menu
- **Click** - Select input fields

## Multiplayer
- Open multiple instances of the game
- Each player can login/register separately
- Real-time gameplay with up to 8 players per server

Enjoy your new desktop game! 🎮🚀