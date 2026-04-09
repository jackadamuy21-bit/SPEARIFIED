# 🚀 Quick Start Guide for Spearified

## Step 1: Install Dependencies

**Option A: Automatic Setup (Windows)**
```bash
setup.bat
```

**Option B: Automatic Setup (macOS/Linux)**
```bash
chmod +x setup.sh
./setup.sh
```

**Option C: Manual Setup**
```bash
# Install server
cd server
npm install
cd ..

# Install app
cd app
npm install
cd ..
```

## Step 2: Start the Server

Open a terminal and run:
```bash
cd server
npm start
```

You should see:
```
🎮 Spearified Server running on port 5000
```

## Step 3: Start the React Development Server

Open a new terminal and run:
```bash
cd app
npm start
```

This will open your browser at `http://localhost:3000`

## Step 4: Start the Electron App (Optional)

For the desktop app experience, open another terminal and run:
```bash
cd app
npm run electron
```

This launches the native desktop application.

## Step 5: Create an Account and Play!

1. **Sign Up**: Click "Sign up here" and create a new account
   - Choose a unique username
   - Create a strong password
   - You'll get a permanent random User ID
   
2. **Login**: Enter your credentials to login

3. **Play**: 
   - Create a new game room or join an existing one
   - Use **W/A/S/D** to move
   - Hold **Shift** to sprint
   - Press **/** to chat

## Quick Tips

- **You get a permanent User ID**: It's a random string that uniquely identifies you forever
- **Special OWNER Badge**: If you name your account exactly `SPEARIFIED`, you'll get a special rainbow badge
- **Chat System**: Press `/` to open chat, type your message, press Enter to send
- **Profanity Filter**: Any swear words are automatically replaced with `#` characters

## Troubleshooting

### "Cannot find module" errors
```bash
cd [server or app]
npm install
```

### Server won't start
- Ensure port 5000 is not in use
- Try: `npm start` again

### React app won't start
- Ensure port 3000 is not in use
- Clear cache: `rm -rf node_modules && npm install`

### Electron won't start
- React dev server must be running on port 3000
- Try: `npm run electron` in the app folder

## Commands Summary

| What | Command |
|------|---------|
| Start Server | `cd server && npm start` |
| Start React | `cd app && npm start` |
| Start Electron | `cd app && npm run electron` |
| Build Electron | `cd app && npm run electron-build` |
| Dev Mode (Server) | `cd server && npm run dev` |

---

**Ready to play? Let's get started! 🎮⚡**
