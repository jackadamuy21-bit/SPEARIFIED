# 🎮 SPEARIFIED - Multiplayer Tag Game

A fast-paced multiplayer tag game built with **Node.js**, **Express**, **WebSocket**, **React**, **Three.js**, and **Electron**.

## 🚀 Quick Start (No npm required!)

If you hate npm and want to play immediately, check out the **npm-free version**:
- See `README_NO_NPM.md` for instructions
- Just needs Python 3 and a web browser
- No installation required!

## Features

✅ **Multiplayer Gameplay** - Real-time multiplayer with up to 8 players per game room  
✅ **Tag Mechanics** - One player is the "tagger", tag others to become the new tagger  
✅ **User System** - Persistent accounts with permanent random user IDs  
✅ **Authentication** - Secure login/signup with password hashing  
✅ **3D Graphics** - Blocky character models rendered with Three.js  
✅ **Movement Controls** - Run and sprint mechanics  
✅ **Chat System** - In-game chat with `/` prefix  
✅ **Profanity Filter** - Swear words are replaced with `#` characters  
✅ **OWNER Badge** - Special rainbow title for the user `SPEARIFIED`  
✅ **Progress Saving** - Persistent account data (level, wins, losses)  
✅ **Desktop App** - Native desktop application with Electron  

## Installation

### Prerequisites

- **Node.js** (v14 or higher)
- **npm** or **yarn**

### Server Setup

```bash
cd server
npm install
npm start
```

Server runs on `http://localhost:5000`

### App Setup

```bash
cd app
npm install
npm start
```

For Electron development:
```bash
npm run electron-dev
```

For production build:
```bash
npm run electron-build
```

## How to Play

### Controls
- **W/A/S/D** - Move forward/left/back/right
- **Shift** - Sprint (faster movement)
- **/key** - Enter chat mode
- **Enter** - Send chat message
- **Escape** - Exit chat mode

### Gameplay
1. Create an account or login
2. Create a new game room or join an existing one
3. **If you're the tagger** (red character), touch other players to tag them
4. **If you're a runner** (green character), avoid being tagged
5. When tagged, you become the new tagger
6. Chat with other players using `/` key

## Game Mechanics

### Tagger
- Red character
- Goal: Tag all runners
- When you tag a runner, they become the new tagger

### Runners
- Green characters
- Goal: Avoid being tagged
- Run and sprint to escape the tagger
- Use sprinting strategically to evade

## Account System

### User ID
- Permanent random string of uppercase letters and numbers
- Cannot be changed
- Used to track your progress

### Username
- Can be chosen during signup
- Unique (cannot duplicate existing usernames)

### Special: SPEARIFIED Username
- If your username is `SPEARIFIED`, you'll get a special rainbow ⭐ **OWNER** badge above your character

## Chat System

Press `/` to open the chat input box and type your message. Use `Shift+Enter` or click send to submit.

### Profanity Filter
Words are automatically filtered and replaced with hashtags (#).

## Project Structure

```
Spearified/
├── server/
│   ├── index.js              # Main server file
│   ├── db.js                 # Database setup
│   ├── GameRoom.js           # Game room logic
│   ├── profanity-filter.js   # Chat filter
│   └── package.json
│
└── app/
    ├── src/
    │   ├── App.js            # Main React component
    │   ├── App.css           # Styles
    │   ├── index.js          # React entry
    │   ├── components/
    │   │   ├── LoginPage.js
    │   │   ├── SignupPage.js
    │   │   ├── MenuPage.js
    │   │   └── GamePage.js
    │   └── utils/
    │       ├── GameClient.js      # WebSocket client
    │       └── BlockyCharacter.js # 3D character model
    ├── public/
    │   ├── index.html
    │   ├── electron.js       # Electron main file
    │   └── preload.js
    └── package.json
```

## Tech Stack

- **Backend**: Node.js, Express, WebSocket (ws)
- **Database**: SQLite3
- **Frontend**: React, Three.js, Axios
- **Desktop**: Electron
- **Authentication**: JWT, bcrypt

## API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new account
- `POST /api/auth/login` - Login to existing account

### Users
- `GET /api/users/:userId` - Get user stats

### Game
- `GET /api/game/rooms` - List available game rooms

### WebSocket Events
- `auth` - Authenticate connection
- `create-room` - Create new game room
- `join-room` - Join existing room
- `start-game` - Start the game
- `player-move` - Send player position
- `chat` - Send chat message

## Database Schema

### Users Table
- id, username, password, user_id, level, coins, gamesPlayed, wins, losses

### Sessions Table
- id, username, user_id, serverTimestamp

### Game Stats Table
- id, user_id, game_id, was_tagger, kills, deaths, duration

## Development

To run both server and app in development:

**Terminal 1:**
```bash
cd server
npm run dev
```

**Terminal 2:**
```bash
cd app
npm start
```

Then, to run Electron:

**Terminal 3:**
```bash
cd app
npm run electron
```

## Building for Production

### Server
```bash
# Just ensure all dependencies are installed
npm install
```

### Desktop App
```bash
cd app
npm run electron-build
```

This generates installers in `app/dist/`.

## Future Enhancements

- [ ] Custom character skins
- [ ] In-game shop with cosmetics
- [ ] Leaderboards
- [ ] Different game modes
- [ ] Sound effects and music
- [ ] Server regions/matchmaking
- [ ] Anti-cheat system
- [ ] Mobile version

## Troubleshooting

**Can't connect to server:**
- Ensure server is running on port 5000
- Check firewall settings
- Verify localhost is accessible

**WebSocket connection fails:**
- Server not running
- Wrong port number
- Network issues

**Electron app won't start:**
- Ensure React dev server is running on port 3000
- Clear node_modules and reinstall
- Check Node.js version

## License

MIT

---

**Enjoy the game! 🎮⚡**
