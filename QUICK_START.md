# ⚡ Quick Start Guide - Jarvis 2.0

## What's New?

✅ **Account System** - Create & manage your account  
✅ **Subscriptions** - Free, Pro, and Premium tiers  
✅ **Chat History** - Save all conversations automatically  
✅ **User Profile** - Track usage and stats  

## 5-Minute Setup

### Step 1: Launch Jarvis
```powershell
cd "c:\Users\REHMAN COMPUTER\Downloads\jarvis"
python main.py
```

### Step 2: Choose Your Path

**Option A: Create Account** (Recommended)
- Click "Create New Account"
- Enter username, email, password
- Click "Register"
- Login with credentials

**Option B: Login Existing Account**
- Enter your username and password
- Click "Login"

**Option C: Guest Mode**
- Click "Continue as Guest"
- Chat without saving data

### Step 3: Start Chatting!
- Type your message in the input field
- Or click "🎤 Listen" for voice input
- Press Enter or click "📤 Send"

## Using New Features

### 💎 Check Subscriptions
1. Click "☰ Menu"
2. Click "💎 Subscriptions"
3. View available plans

### 📜 View Chat History
1. Click "☰ Menu"
2. Click "📜 Chat History"
3. Browse all past conversations

### 👤 Account Info
1. Click "☰ Menu"
2. Click "👤 Account Info"
3. See your stats and settings

## Tips & Tricks

### Free Tier (100 queries/month)
- Perfect for casual users
- Track usage in Account Info
- Upgrade when needed
- Resets monthly

### Pro Tier ($9.99/month)
- 1000 queries = 33/day
- Ad-free experience
- Priority support
- Great for regular users

### Premium Tier ($19.99/month)
- 10,000 queries = 333/day
- All features unlocked
- 24/7 support
- Early access to new features

## Common Tasks

**Query Usage Status**
```
Menu → Account Info → See "Queries Used"
```

**Export Chat**
```
Menu → Chat History → (Select conversations)
Right-click → Export (coming soon)
```

**Change Subscription**
```
Menu → Subscriptions → Click "Upgrade"
```

**Clear Session**
```
Click "🗑️ Clear" to clear current conversation
```

## Troubleshooting

**Database Error?**
- Delete `jarvis_data.db`
- Restart Jarvis
- It rebuilds automatically

**Can't Login?**
- Check username spelling
- Passwords are case-sensitive
- Use "Create New Account" if forgot password

**Query Limit Reached?**
- Upgrade to Pro/Premium
- Free tier resets monthly
- Check usage in Account Info

## File Organization

```
jarvis/
├── main.py                 ← Run this
├── database.py            ← Stores user data
├── account_manager.py     ← Manages accounts
├── auth_ui.py            ← Login screens
├── jarvis_data.db        ← Your data (auto-created)
└── NEW_FEATURES.md       ← Full documentation
```

## First-Time Checklist

- [ ] Installed all dependencies
- [ ] Set OPENROUTER_API_KEY environment variable
- [ ] Created account or logged in
- [ ] Tested voice input
- [ ] Checked subscription options
- [ ] Viewed chat history

## Need Help?

1. **Forgot password?** → Create new account
2. **Chat not saving?** → Ensure you're logged in
3. **Can't use voice?** → Check microphone permissions
4. **Limited queries?** → Upgrade subscription

---

**Ready to use Jarvis 2.0?**  
Start with: `python main.py`

Questions? Check `NEW_FEATURES.md` for detailed documentation!
