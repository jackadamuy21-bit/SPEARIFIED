# Spearified v2 - Admin System Update

## What's New

### 🔨 Admin Panel System
- **Exclusive to SPEARIFIED user**: Full admin control over the game
- **Press P** to toggle admin panel in-game
- **Real-time player management**: Kick, ban, fling, tag, fly control

### 🎮 Special Game Commands
1. **Meteor Shower** - Rain meteors on the map, fling players skyward
2. **Disco Mode** - Rainbow flashing effects, party atmosphere
3. **Fling Command** - Launch players in random directions
4. **Fly Mode** - Allow players to fly with yellow wing effects
5. **Force Tag** - Make any player the tagger instantly
6. **Message Broadcast** - Send system messages to all players

### 🆔 Username Validation System
- **No Inappropriate Names**: Filter blocks offensive/reserved words
- **No Duplicate Names**: Exact duplicates prevented
- **No Similar Names**: Names too close to existing ones blocked
- **L33t Speak Detection**: Catches variations like `4dm1n` or `s3x`
- **Character Restrictions**: Only alphanumeric + underscore
- **Length Limits**: 3-20 characters only

### 🚫 Ban System
- **Permanent Bans**: Remove and ban players from server
- **Database Persistent**: Bans survive server restart
- **Ban Reasons**: Track why players were banned
- **Unban Support**: Admins can unban players

### ⭐ Owner Badge
- If username is `SPEARIFIED` (exactly):
  1. Get rainbow glowing **⭐ OWNER ⭐** badge
  2. Unlock admin panel access
  3. Gain all admin powers
  4. Can execute any command

## File Changes

### Backend (Server)

#### New Files
- `server/admin.js` - Admin commands system
- `server/username-validator.js` - Username validation with inappropriate word filter

#### Updated Files
- `server/index.js` - Added admin command handling, username validation in signup, ban checking
- `server/db.js` - Added `banned_users` table
- `server/GameRoom.js` - Added broadcast methods for system messages and special events

### Frontend (App)

#### New Files
- `app/src/components/AdminPanel.js` - Admin control interface

#### Updated Files
- `app/src/App.css` - Added admin panel styles, animated effects
- `app/src/components/GamePage.js` - Integrated admin panel, event handlers for special effects
- `app/src/components/SignupPage.js` - Added username rules display
- `app/src/utils/GameClient.js` - Added admin command support and event handlers

## Database Changes

### New Table: banned_users
```sql
CREATE TABLE banned_users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id TEXT UNIQUE NOT NULL,
  reason TEXT,
  banned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  expires_at DATETIME
)
```

## API Changes

### New WebSocket Messages

#### Client → Server
- `admin-command`: Execute admin command
  ```json
  {
    "type": "admin-command",
    "command": "kick PlayerName reason"
  }
  ```

#### Server → Client
- `system-message`: System announcement
  ```json
  {
    "type": "system-message",
    "message": "[ADMIN]: message text"
  }
  ```
- `meteor-shower`: Meteor spawn event
  ```json
  {
    "type": "meteor-shower",
    "data": { "meteors": [...] }
  }
  ```
- `disco-mode`: Disco toggle event
  ```json
  {
    "type": "disco-mode",
    "data": { "enabled": true }
  }
  ```
- `admin-response`: Admin command result
  ```json
  {
    "type": "admin-response",
    "success": true,
    "message": "response text"
  }
  ```

## Configuration

### Username Validator Configuration
Edit `server/username-validator.js` to add/remove blocked words:
```javascript
const INAPPROPRIATE_WORDS = [
  'word1', 'word2', 'word3' // Add your words here
];
```

### Similarity Threshold
Edit `server/username-validator.js` to adjust:
```javascript
const threshold = 3; // Max distance for "similar"
```

### Ban Table Management
View bans in database:
```sql
SELECT * FROM banned_users;
```

Clean expired bans:
```sql
DELETE FROM banned_users WHERE expires_at < datetime('now');
```

## Security Notes

⚠️ **Important Reminders**:

1. **Single Admin User**: Only SPEARIFIED can use admin commands
2. **SQL Injection**: All user input is parameterized
3. **Rate Limiting**: Consider adding for production
4. **Logging**: All admin actions should be logged
5. **Audit Trail**: Ban reasons stored for accountability

## Performance Considerations

- **Meteor Shower**: Creates temporary mesh objects (~20-50 per command)
- **Disco Mode**: Toggle switches background animation (low overhead)
- **Username Validation**: Levenshtein distance O(n*m) complexity
- **Ban Checking**: Database lookup on connection (should be cached)

## Future Enhancements

- [ ] Time-based bans
- [ ] Mute system
- [ ] Warning system before ban
- [ ] Admin logs viewer
- [ ] Multi-admin support
- [ ] Command history/rollback
- [ ] Custom game rules
- [ ] Anti-cheat system
- [ ] Player reputation system
- [ ] Profanity auto-mute

## Troubleshooting

### Admin Commands Not Working
1. Verify username is exactly `SPEARIFIED`
2. Check you're in a game room
3. Verify player names in command match exactly (case-sensitive)
4. Check server console for errors

### Meteor Shower Not Showing
- Check WebSocket connection
- Verify `meteor-shower` event received
- Check browser console for errors

### Disco Mode Not Toggling
- Confirm toggle message received
- Verify CSS animation enabled
- Check graphics settings

### Ban Not Taking Effect
- Verify user ID in database
- Check `expires_at` column is NULL or future timestamp
- Restart server or re-login to trigger check

## Documentation Files

- `QUICKSTART.md` - Quick setup guide
- `README.md` - Full project documentation
- `CONFIG.md` - Configuration guidelines
- `ADMIN_GUIDE.md` - Comprehensive admin system guide (NEW)

## Keyboard Shortcuts Summary

| Key | Action |
|-----|--------|
| **P** | Toggle Admin Panel (SPEARIFIED only) |
| **W/A/S/D** | Move |
| **Shift** | Sprint |
| **/** | Chat |
| **Enter** | Send chat/command |
| **Esc** | Close chat |

## Version Info

- **Spearified v2**
- **Released**: April 9, 2026
- **Features**: Admin system, username validation, ban system
- **Breaking Changes**: None

---

**Ready to administrate? Press P to open the admin panel!** 🎮⚡

For detailed admin commands, see [ADMIN_GUIDE.md](./ADMIN_GUIDE.md)
