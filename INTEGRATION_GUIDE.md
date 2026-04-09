# Spearified Integration Guide - Admin System

## Complete Feature Overview

Your Spearified game now has a complete admin system with powerful moderation and special effects. Here's how everything works together:

---

## 🎯 Core Components

### 1. Username Validation System
**File**: `server/username-validator.js`

Validates usernames on signup with three layers:
1. **Word Filter**: Blocks inappropriate words
2. **Similarity Check**: Prevents names like `Player1` if `Player` exists
3. **Format Validation**: Only alphanumeric + underscore, 3-20 chars

**Result**: Clean, appropriate usernames only

### 2. Ban System
**Files**: 
- `server/index.js` - Ban checking
- `server/db.js` - Database table
- `server/admin.js` - Ban commands

When user connects:
1. Check if `user_id` in `banned_users` table
2. If banned and not expired, disconnect with message
3. Ban stored in database persists across server restarts

**Result**: Permanent moderation

### 3. Admin Commands System
**File**: `server/admin.js`

Provides all admin functionality:
- **Player Management**: kick, ban, unban
- **Special Effects**: message, meteor, disco, fling, tag, fly, unfly
- **Server Control**: shutdown, help

Each command validates inputs and broadcasts results to all players.

**Result**: Complete server control

### 4. Admin Panel UI
**File**: `app/src/components/AdminPanel.js`

Provides interface with:
- Real-time player list
- Quick action buttons
- Custom command input
- Command output log

**Result**: Easy admin management

---

## 🔄 Data Flow Example: Ban Command

```
1. Admin presses "Ban" button in AdminPanel
   ↓
2. AdminPanel sends: { type: "admin-command", command: "ban PlayerName reason" }
   ↓
3. Server receives message in WebSocket handler
   ↓
4. Validates user is "SPEARIFIED"
   ↓
5. AdminCommands.executeCommand() processes ban
   ↓
6. Inserts into banned_users table
   ↓
7. Removes player from room
   ↓
8. Broadcasts system message to all players
   ↓
9. Returns response to admin
   ↓
10. Admin panel displays result in log
```

---

## 🎮 Player Experience

### Regular Player
```
Signup → Validate Username → Create Account → Login → Join Game → Play
```

If username is inappropriate or too similar:
```
❌ "Username contains inappropriate content"
or
❌ "Username is too similar to an existing username"
```

### Admin Player (SPEARIFIED)
```
Signup as "SPEARIFIED" → Login → Join Game → Press P → Admin Panel Opens
```

In admin panel:
- See all players
- Click buttons to execute commands
- Or type custom commands
- View results in log

---

## 📊 Database Schema Overview

### users table
```
Standard fields + user_id (permanent)
```

### banned_users table
```
user_id → reason → banned_at → expires_at (NULL = permanent)
```

### game_stats table
```
Tracks kills, deaths, tagger status, duration
```

---

## 🌟 Special Effects Implementation

### Meteor Shower
```
Server generates 20 meteors with position + damage radius
↓
Sends meteor-shower event to all clients
↓
Client creates THREE.Mesh for each meteor
↓
Animation: Falls from sky to ground in 2 seconds
↓
Server applies velocity to nearby players (fling effect)
```

### Disco Mode
```
Admin sends: /admin disco
↓
Server broadcasts disco-mode event (enabled: true)
↓
Client sets discoMode state = true
↓
CSS animation triggers: rainbow color changes every 100ms
↓
Apply to scene background + character materials
```

### Fly Mode
```
Admin sends: /admin fly PlayerName
↓
Server marks player.isFlying = true
↓
Player object included in game-state broadcast
↓
Client renders yellow rotating wing effect
↓
Flight data persists until /admin unfly sent
```

---

## 🔐 Security Features

### 1. Admin-Only Commands
```javascript
if (username === 'SPEARIFIED') {
  // Process admin command
} else {
  // Send error response
}
```

### 2. Input Validation
- Username validated before insertion
- Command parameters checked for validity
- Player names verified before acting

### 3. Database Security
- All queries use parameterized statements
- Prevents SQL injection
- User input never directly in query

### 4. Ban Persistence
- Stored in database
- Checked on every connection
- Cannot bypass by re-logging

---

## 🚀 Deployment Checklist

- [ ] Update `JWT_SECRET` in `server/index.js` for production
- [ ] Change inappropriate words list if needed
- [ ] Set up database backups
- [ ] Enable CORS for production domain
- [ ] Add rate limiting middleware
- [ ] Set up admin logging
- [ ] Test all commands
- [ ] Verify username validation works
- [ ] Test ban system with test account
- [ ] Verify special effects render correctly

---

## 📝 Admin Best Practices

1. **Document Bans**: Always provide reason
2. **Progressive Discipline**: Warn → Kick → Ban
3. **Announce Actions**: Use broadcast message
4. **Monitor Behavior**: Check for toxic patterns
5. **Review Bans**: Periodically check ban list
6. **Fair Moderation**: Apply rules consistently

---

## 🐛 Debugging Commands

### View all bans (SQL)
```sql
SELECT user_id, reason, banned_at FROM banned_users;
```

### Clear all bans (SQL)
```sql
DELETE FROM banned_users;
```

### Check active players (Server console)
```
Logs: [USERNAME] joined
      [USERNAME] disconnected
```

### Monitor admin commands (Server)
Enable logging in `server/admin.js` executeCommand()

---

## 🎨 Customization Options

### Change Blocked Words
Edit `server/username-validator.js`:
```javascript
const INAPPROPRIATE_WORDS = [
  'add', 'your', 'words', 'here'
];
```

### Adjust Similarity Threshold
Edit `server/username-validator.js`:
```javascript
const threshold = 3; // Lower = stricter (more blocked)
```

### Modify Admin Panel Layout
Edit `app/src/components/AdminPanel.js` and `app/src/App.css`

### Change Command Responses
Edit `server/admin.js` response messages

### Adjust Special Effects
Edit `app/src/components/GamePage.js` effect functions

---

## 📚 Related Files Summary

| File | Purpose |
|------|---------|
| `server/admin.js` | Admin command logic |
| `server/username-validator.js` | Username filtering |
| `server/index.js` | Server entry, auth, ban checking |
| `server/db.js` | Database schema |
| `server/GameRoom.js` | Game room + broadcast |
| `app/src/components/AdminPanel.js` | Admin UI |
| `app/src/components/GamePage.js` | Game + effects |
| `app/src/utils/GameClient.js` | WebSocket client |

---

## ✨ Features at a Glance

✅ **Username Validation**: Smart filtering + uniqueness  
✅ **Admin Panel**: Easy-to-use interface  
✅ **Ban System**: Permanent, database-backed  
✅ **Special Effects**: Meteors, disco, flying  
✅ **Moderation**: Kick, ban, message broadcast  
✅ **Owner Badge**: ⭐ OWNER ⭐ with rainbow effect  
✅ **Real-time**: WebSocket-powered instant updates  
✅ **Persistent**: Bans and accounts saved  

---

## 🎬 Quick Demo Flow

1. **Create SPEARIFIED Account**
   - Signup page accepts it
   - Unique username stored
   - Rainbow badge unlocked

2. **Create Game Room**
   - Join / create room
   - See players list

3. **Open Admin Panel**
   - Press P key
   - Panel appears top-right
   - See all players

4. **Try Commands**
   - Click "Meteor Shower" → meteors fall
   - Click "Disco" → rainbow effects
   - Click "Fling" on player → launches them
   - Use "Kick" / "Ban" for moderation

5. **Test Bans**
   - Ban a player
   - Test account tries to rejoin
   - Gets banned message
   - Cannot play

6. **Test Username Filter**
   - Try to create "Admin" account → blocked
   - Try "Player" then "Player1" → Player1 blocked
   - Try "sex123" → blocked
   - Try "CoolDude99" → accepted ✅

---

## 🏁 You're All Set!

Your Spearified game now has:
- ✅ Complete admin system
- ✅ Smart username validation  
- ✅ Ban system for moderation
- ✅ Special game effects
- ✅ Professional moderator tools

**To get started**: Run `setup.bat` and follow QUICKSTART.md

**For admin details**: Read ADMIN_GUIDE.md

**Happy moderating!** 🎮⚡
