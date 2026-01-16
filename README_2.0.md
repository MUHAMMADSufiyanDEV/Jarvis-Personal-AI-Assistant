# 🤖 JARVIS - Enhanced AI Assistant 2.0

> Your personal AI assistant with professional account management, subscriptions, and chat history!

## ✨ What's New in 2.0?

### 🔐 Account System
- Create personalized accounts
- Secure login with password hashing
- Guest mode for quick access
- User profile with statistics

### 💎 Subscription Tiers
- **Free**: 100 queries/month, basic features
- **Pro**: 1,000 queries/month, ad-free, priority support
- **Premium**: 10,000 queries/month, all features, 24/7 support

### 📜 Chat History
- Automatic conversation saving (like ChatGPT!)
- Browse all past conversations
- Session-based organization
- View statistics and analytics

### 👤 User Features
- Account information dashboard
- Usage statistics and tracking
- Query limit monitoring
- Last login tracking

## 🚀 Quick Start

### Installation
```bash
cd "c:\Users\REHMAN COMPUTER\Downloads\jarvis"
pip install -r requirements.txt
```

### First Run
```bash
python main.py
```

### Choose Your Path
1. **Create Account** - New users, recommended for saving progress
2. **Login** - Returning users
3. **Guest Mode** - Try without account

## 💬 Features

### Core AI Capabilities
✅ Answer any question using OpenRouter AI  
✅ Explain concepts and provide information  
✅ Write code and technical help  
✅ Voice input and output  
✅ Search Google and Wikipedia  
✅ Open applications  
✅ System control commands  
✅ Beautiful modern UI  

### Account Features
✅ User registration and authentication  
✅ Password security with hashing  
✅ Session management  
✅ Personal chat history  
✅ Usage statistics  
✅ Subscription management  
✅ Tier-based features  

## 🎯 Use Cases

### Free Tier Users
- Casual questions and learning
- Basic AI assistance
- Limited daily queries (3/day avg)
- Perfect for trying it out

### Pro Tier Users
- Professional use cases
- Daily work assistance
- Ad-free experience
- ~33 queries per day available

### Premium Tier Users
- Enterprise use cases
- Unlimited access (333+ queries/day)
- Priority support
- Early access to new features

## 📊 Subscription Comparison

| Feature | Free | Pro | Premium |
|---------|------|-----|---------|
| Monthly Queries | 100 | 1,000 | 10,000 |
| Voice Input | ✓ | ✓ Priority | ✓ Priority |
| Chat History | 7 days | Unlimited | Unlimited |
| Ad-Free | ✗ | ✓ | ✓ |
| Support | Basic | Priority | 24/7 Premium |
| Cost | Free | $9.99 | $19.99 |

## 📁 Project Structure

```
jarvis/
├── main.py                    # Main application
├── database.py               # Database & persistence
├── account_manager.py        # User & subscription logic
├── auth_ui.py               # Authentication screens
├── requirements.txt          # Dependencies
├── jarvis_data.db           # User database (auto-created)
├── NEW_FEATURES.md          # Feature documentation
├── QUICK_START.md           # Quick start guide
└── SETUP_OPENROUTER.md      # API setup guide
```

## 🔧 Configuration

### API Key Setup
Required for AI features to work:

```powershell
# Option 1: Set environment variable in PowerShell
$env:OPENROUTER_API_KEY="your_key_here"
python main.py
```

```powershell
# Option 2: Permanent (Windows)
setx OPENROUTER_API_KEY "your_key_here"
```

See `SETUP_OPENROUTER.md` for detailed setup instructions.

## 📚 Commands & Features

### Chat Input
- Type any question or command
- Press Enter to send
- Use 🎤 button for voice input

### Available Commands
- **Time/Date**: "What time is it?"
- **Search**: "Search for Python tutorials"
- **Wikipedia**: "Wikipedia history of AI"
- **Open Apps**: "Open Chrome", "Open Notepad"
- **System Control**: "Increase volume", "Lock screen"

### Menu Features (☰ Button)
- **💎 Subscriptions** - View and upgrade plans
- **📜 Chat History** - Browse past conversations
- **👤 Account Info** - View profile and stats
- **🚪 Logout** - Sign out of account

## 🔒 Security & Privacy

- Passwords stored with SHA-256 hashing
- Local SQLite database (your data stays local)
- Secure session management
- User data isolation
- No unnecessary data collection

## 🐛 Troubleshooting

### Database Error
Delete `jarvis_data.db` and restart - it rebuilds automatically.

### Can't Login
- Check username spelling (case-sensitive)
- Ensure password is correct
- Password minimum is 6 characters

### API Not Working
- Set `OPENROUTER_API_KEY` environment variable
- Check internet connection
- Verify API key is valid at openrouter.ai

### Voice Not Working
- Check microphone is connected
- Verify microphone permissions in Windows
- Test microphone in Windows settings

### Query Limit Reached (Free Users)
- Upgrade to Pro or Premium tier
- Free tier resets monthly
- Check usage in Account Info

## 📖 Documentation

- **NEW_FEATURES.md** - Complete feature documentation
- **QUICK_START.md** - 5-minute quick start guide
- **SETUP_OPENROUTER.md** - API configuration
- **IMPLEMENTATION_SUMMARY.md** - Technical details

## 🎮 How to Use

### First Time
```
1. Run: python main.py
2. Click "Create New Account"
3. Fill in details (username, email, password)
4. Login with credentials
5. Start chatting!
```

### View Chat History
```
1. Login to your account
2. Click "☰ Menu"
3. Click "📜 Chat History"
4. Browse all conversations
```

### Upgrade Subscription
```
1. Click "☰ Menu"
2. Click "💎 Subscriptions"
3. Choose your plan
4. Click "Upgrade"
```

## 🌟 Key Highlights

- **ChatGPT-like Experience**: Save and browse all conversations
- **Professional Tiers**: Free, Pro, and Premium options
- **Secure Accounts**: Password-protected user accounts
- **Beautiful UI**: Modern dark theme with intuitive controls
- **Voice Support**: Speak and listen to responses
- **Local Database**: Your data is stored locally, not on cloud
- **Works Offline**: Core features work without internet (with limited AI)

## 🚀 Getting Started Now

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key (if not already set)
$env:OPENROUTER_API_KEY="sk-or-v1-..."

# Launch Jarvis
python main.py
```

### First Steps
1. ✅ Create an account or login
2. ✅ Try asking a question
3. ✅ Check your chat history
4. ✅ Explore subscription plans
5. ✅ Customize your preferences

## 💡 Tips

- **Free Users**: Get 3-4 queries per day on average
- **Pro Users**: Perfect for daily work assistance
- **Premium Users**: No query limits, full access to all features
- **Voice Input**: Great for hands-free operation
- **Chat History**: Perfect for reference and learning

## 🤝 Support

For issues or questions:
1. Check the documentation files
2. Review troubleshooting section
3. Check Account Info for subscription details
4. Contact support (available with Pro/Premium tiers)

## 📈 Future Roadmap

- Payment integration for subscriptions
- Cloud backup of chat history
- Advanced search and filtering
- Export conversations as PDF
- Multi-device synchronization
- Custom themes and personalization
- Advanced analytics dashboard
- Mobile app companion

## 📄 License

See `License free.txt` and `License premium.txt` for details.

## 🎉 Enjoy Jarvis 2.0!

Experience the power of AI with professional account management and chat history, all in one beautiful application.

**Ready to get started?** Run `python main.py` now!

---

**Version**: 2.0+  
**Status**: Active & Ready  
**Last Updated**: January 2026  
**Built with**: Python, Tkinter, OpenRouter AI, SQLite
