# Spearified Admin System Documentation

## Overview

The Spearified Admin System gives the user with username **`SPEARIFIED`** complete control over the game server and player management. This user has special powers and can execute commands to manage the game.

## Admin Features

### 1. Admin Panel Access
- **Keyboard Shortcut**: Press **P** in-game to toggle the admin panel
- **Visibility**: Only visible to the SPEARIFIED user
- **Location**: Top-right corner of the screen when open
- **Orange Border**: Easy to identify with orange glow effect

### 2. Player Management

#### Quick Actions
The admin panel shows all players in the current room with quick action buttons:

| Button | Action | Effect |
|--------|--------|--------|
| **Kick** | Remove player from game | Player disconnected, message broadcast |
| **Ban** | Remove and ban player | Player cannot rejoin |
| **Fling** | Launch player | Sends player flying in random direction |
| **Tag** | Make player the tagger | Player becomes "it" immediately |
| **Fly** | Enable flight mode | Player can fly above the map |
| **UnFly** | Disable flight mode | Player returns to normal movement |

#### Ban System
- Banned players cannot rejoin the server
- Bans are stored in the database
- System-wide bans apply to all game rooms

### 3. Special Commands

#### Meteor Shower
```
/admin meteor 30
```
- Spawns meteors from the sky
- Affects all players in the room
- Players flinged upward when hit
- Damage radius: 5 units
- Visual effect: Glowing falling projectiles

#### Disco Mode
```
/admin disco
```
- Toggles disco mode on/off
- Screen background flashes rainbow colors
- All characters flash rainbow colors
- Duration: Until toggled off or command sent again
- Creates a party atmosphere

#### Broadcast Message
```
/admin message [your message here]
```
- Sends a system message to all players
- Displays with [ADMIN] prefix
- Useful for announcements

### 4. Server Control

#### Shutdown
```
/admin shutdown
```
- Shuts down the entire server
- Broadcasts warning message
- Server stops after 2 seconds
- **Use carefully!**

### 5. Command Format

All admin commands follow this format:
```
/admin [action] [target/params] [optional params]
```

### Full Command List

```
/admin message [text]              - Broadcast a message
/admin ban [username] [reason]     - Ban a player (reason optional)
/admin unban [username]            - Unban a player
/admin kick [username] [reason]    - Kick a player (reason optional)
/admin fling [username] [force]    - Fling a player (force optional, default 50)
/admin tag [username]              - Make player the tagger
/admin fly [username]              - Enable fly mode
/admin unfly [username]            - Disable fly mode
/admin meteor [count]              - Spawn meteors (count optional, default 20)
/admin disco                       - Toggle disco mode
/admin shutdown                    - Shutdown server
/admin help                        - Show command help
```

## Username Validation System

### Inappropriate Usernames
The following types of usernames are blocked:

#### Blocked Words
- Admin/moderator titles
- Offensive/sexual content
- Racist/discriminatory terms
- Hacking-related terms
- Spam-related terms
- Violence/self-harm terms

#### Invalid Formats
- Too short (< 3 characters)
- Too long (> 20 characters)
- Special characters (only alphanumeric and `_`)
- L33t speak variants of blocked words

### Duplicate/Similar Names
- Usernames must be unique
- Similar usernames are blocked with **Levenshtein distance**
- Maximum similarity distance: 3
- Examples of blocked similar names:
  - `Player` and `Player1` (too close)
  - `John` and `Jon` (too close)
  - `Admin` and `Admim` (close with typo)

### Examples

✅ **Allowed Usernames**:
- `Player123`
- `Ninja_Master`
- `CoolDude99`

❌ **Blocked Usernames**:
- `sex` (inappropriate)
- `Admin` (reserved)
- `Play` (too short)
- `VeryLongUserNameThatIsTooLong` (too long)
- `Player1` (if `Player` exists)
- `n1gga` (l33t speak filter)

## SPEARIFIED Owner Badge

The user with username **`SPEARIFIED`** gets:
- ⭐ **OWNER** badge above character
- Rainbow-colored title
- Glowing animation effect
- Admin panel access
- Full server control

## Admin Panel UI

### Tabs

#### Players Tab
- Lists all players in the current room
- Shows tagger and flying status
- Quick action buttons for each player
- Player count display

#### Commands Tab
- Quick command buttons for special effects
- Custom command input field
- Command execution output log
- Help command reference

### Features

- **Real-time Updates**: Shows current players in room
- **Command Log**: Displays executed commands with timestamps
- **Status Indicators**: Shows which players have special status (tagger, flying)
- **Error Handling**: Shows error messages if command fails

## Flying Mechanic

### Enabling Flight
```
/admin fly [username]
```

### Visual Indicators
- Flying players have **yellow wings** that rotate
- Wings are visible on character model
- Indicates flight status to all players

### Disabling Flight
```
/admin unfly [username]
```

### Movement with Flight
- Flying players move significantly faster
- Can reach areas normally inaccessible
- Same sprint/walk mechanics apply

## Special Effects

### Meteor Shower Visuals
- Meteors spawn from top of map
- Glowing orange projectiles
- Trail effects as they fall
- Impact animation when landing

### Disco Mode
- **Background**: Black with pulsing colors
- **Character Colors**: Rainbow flashing
- **Frequency**: Every 1 second cycle
- **Atmosphere**: Creates playful game mode

## Ban System Details

### Database Storage
Bans are stored in `banned_users` table:
```
- user_id: Unique player identifier
- reason: Admin-provided ban reason
- banned_at: Timestamp of ban
- expires_at: Expiration time (optional, permanent if NULL)
```

### Ban Enforcement
- Checked on connection attempt
- Prevents account from joining any room
- Message shown: "You are banned from the server"

### Unban Command
```
/admin unban [username]
```
- Removes ban from database
- User can rejoin immediately

## Security & Moderation

### Admin Authority
- SPEARIFIED user has absolute authority
- Cannot be overridden by other players
- Commands execute immediately

### Limits
- Ban duration: Permanent by default
- Kick reason: For audit trail
- Message broadcast: No character limit

### Logging
All admin actions are logged with:
- Timestamp
- Admin username
- Action type
- Target player (if applicable)
- Reason (if applicable)

## Troubleshooting

### Admin Panel Won't Open
- Verify username is exactly `SPEARIFIED`
- Confirm you're in a game room
- Try pressing **P** key again
- Check if admin panel is already open (look top-right)

### Commands Not Working
- Verify command syntax
- Check player username spelling (case-sensitive with spaces)
- Ensure player is in current room
- View command log for error messages

### Meteor Shower Not Showing
- Check render settings
- Ensure graphics are enabled
- Disable any overlays blocking view

### Disco Mode Colors Not Showing
- Update graphics drivers
- Lower screen resolution
- Try restarting client

## Best Practices

1. **Use Ban Sparingly**: Only ban for serious violations
2. **Give Warnings**: Kick players before banning
3. **Broadcast Reasons**: Tell other players why actions were taken
4. **Monitor Behavior**: Watch for rule violations
5. **Document Bans**: Use reason field for audit trail

## Admin Commands Cheat Sheet

| Command | Shortcut | Result |
|---------|----------|--------|
| Message | - | /admin message Hello world! |
| Ban | - | /admin ban PlayerName Rule violation |
| Kick | - | /admin kick PlayerName Be respectful |
| Fling | - | /admin fling PlayerName 100 |
| Tag | - | /admin tag PlayerName |
| Fly | - | /admin fly PlayerName |
| UnFly | - | /admin unfly PlayerName |
| Meteor | 🌠 | /admin meteor 50 |
| Disco | 🕺 | /admin disco |
| Shutdown | 🛑 | /admin shutdown |

---

**Admin Responsibility**: With great power comes great responsibility. Use admin commands fairly and consistently!
