# Spearified Configuration

## Server Configuration

### Ports
- Server: 5000
- WebSocket: 5000 (same as HTTP)

### Database
- Type: SQLite3
- Location: `server/spearified.db`
- Auto-initializes on first run

### Authentication
- Method: JWT + bcrypt
- JWT Secret: Change in production! (currently hardcoded in index.js)
- Token Expiry: 7 days

## Game Configuration

### Game Room Settings
- Max players per room: 8
- Game duration: 5 minutes
- Initial tagger: First player to join

### Game Physics
- Collision distance: 3 units
- Player movement speed: 0.001-0.002 units/tick
- Sprint multiplier: 2x

### Chat System
- Max chat history: 50 messages per session
- Profanity filter: Enabled by default
- Input: Triggered with `/` key

## Special Usernames

### SPEARIFIED (Owner)
- Username: `SPEARIFIED` (case-sensitive)
- Effect: Rainbow badge above character
- Badge text: `⭐ OWNER ⭐`

## User ID Format

- Type: Random alphanumeric string
- Length: 12 characters
- Format: `[A-Z0-9]{12}`
- Permanence: Forever (cannot be changed)
- Collision probability: < 1 in 64 trillion

## Database

### Connection String
SQLite auto-creates at: `server/spearified.db`

### Tables

**users**
```
- id (primary key)
- username (unique)
- password (bcrypt hash)
- user_id (unique)
- level
- coins
- gamesPlayed
- wins
- losses
- createdAt
```

**sessions**
```
- id (primary key)
- username
- user_id
- serverTimestamp
```

**game_stats**
```
- id (primary key)
- user_id
- game_id
- was_tagger
- kills
- deaths
- duration
```

## WebSocket Events

### Client → Server
- `auth`: Authenticate connection
- `join-room`: Join game room
- `create-room`: Create new room
- `start-game`: Start the game
- `player-move`: Update player position
- `chat`: Send chat message

### Server → Client
- `room-joined`: Confirmation of room join
- `game-started`: Game has started
- `game-state`: Current game state
- `tag-event`: Player was tagged
- `chat`: Chat message from another player
- `error`: Error message

## Performance Tuning

### Server
- Update tick rate: Real-time (event-driven)
- Collision check: Every player move
- Memory per room: ~50KB

### Client
- Render FPS: 60 (Three.js)
- Update frequency: 20-30Hz
- Camera smooth follow: Lerp 0.1

## Security Considerations

⚠️ **IMPORTANT FOR PRODUCTION**

1. Change JWT_SECRET in `server/index.js`
2. Use environment variables for sensitive data
3. Add CORS configuration
4. Implement rate limiting
5. Add input validation
6. Use HTTPS for production
7. Implement anti-cheat measures
8. Add server-side position validation

## Deployment

### Server Deployment
1. Install Node.js on server
2. Install dependencies: `npm install --production`
3. Set environment variables:
   ```
   ENVIRONMENT=production
   JWT_SECRET=your-secret-key
   PORT=5000
   ```
4. Start with: `node index.js`
5. Use PM2 or systemd for process management

### App Electron Build
```bash
cd app
npm run electron-build
```

This creates installers in `app/dist/`

## Environment Variables

Create a `.env` file in the server directory:

```
ENVIRONMENT=development
JWT_SECRET=your-super-secret-key-change-this
PORT=5000
DATABASE_PATH=./spearified.db
```

## Monitoring

### Metrics to Track
- Active connections
- Games in progress
- Average game duration
- Player retention
- Chat messages per game

### Logs
All server events are logged to console. For production, integrate with:
- Winston
- Morgan
- Datadog
- CloudWatch

---

For questions, see [README.md](./README.md) or [QUICKSTART.md](./QUICKSTART.md)
