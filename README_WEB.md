# 🤖 Jarvis AI Assistant - Web Version

Convert your desktop Jarvis to a live web app accessible to everyone on the internet!

## 🌐 What's New

This web version includes:
- ✅ Modern web interface (works on desktop, tablet, mobile)
- ✅ User registration & authentication
- ✅ Cloud deployment ready
- ✅ Real-time chat with AI
- ✅ Chat history & export
- ✅ Subscription management
- ✅ Database persistence

## 🚀 Quick Start (Local)

### Windows Users:
```bash
# Simply double-click:
start.bat
```

Then open: http://localhost:5000

### Mac/Linux Users:
```bash
# Run the start script
bash start.sh
```

Then open: http://localhost:5000

### Manual Setup:
```bash
# 1. Install dependencies
pip install -r requirements-web.txt

# 2. Set API key
set OPENROUTER_API_KEY="your_key_here"

# 3. Run
python app.py

# 4. Open browser
# http://localhost:5000
```

## 🌍 Deploy to Internet

### Choose Your Platform:

**Quick & Easy (Recommended):**
- [Railway.app](https://railway.app) - 5 min setup
- [Render.com](https://render.com) - 5 min setup  
- [Heroku](https://heroku.com) - 10 min setup

**See DEPLOYMENT_GUIDE.md for detailed instructions**

### TL;DR Deploy Steps:

1. Fork/clone this repo to GitHub
2. Go to Railway/Render/Heroku
3. Connect your GitHub repo
4. Add environment variables (OPENROUTER_API_KEY)
5. Deploy (automatic!)
6. Get your live URL
7. Share with the world!

## 📦 What's Inside

```
jarvis/
├── app.py                 # Flask backend (handles all requests)
├── database.py           # User & chat data storage
├── account_manager.py    # Authentication
├── templates/
│   └── index.html        # Modern web UI
├── jarvis_data.db        # SQLite database (auto-created)
├── requirements-web.txt  # Python packages
├── Procfile              # Cloud deployment config
└── DEPLOYMENT_GUIDE.md   # Full deployment guide
```

## 🔑 Features

### For Users:
- 🎭 Register/login with username & password
- 💬 Chat with AI in real-time
- 📜 View chat history
- 📤 Export conversations (TXT/JSON)
- 💎 Upgrade subscription tier
- 📱 Works on any device

### For Developers:
- 🔐 Secure authentication
- 🗄️ SQLite database
- 🔌 RESTful API
- 📊 Chat statistics
- 🚀 Production-ready

## 🎯 Subscription Tiers

| Feature | Free | Pro | Premium |
|---------|------|-----|---------|
| Queries/Month | 100 | 1,000 | 10,000 |
| Voice Support | ✅ | ✅ | ✅ |
| Ad-Free | ❌ | ✅ | ✅ |
| Priority Support | ❌ | ✅ | ✅ |
| Export | ✅ | ✅ | ✅ |
| Price | Free | $9.99 | $19.99 |

## 🔒 Security

- ✅ Passwords hashed with SHA-256
- ✅ Session management
- ✅ CORS enabled (customizable)
- ✅ Environment variables for secrets
- ✅ No sensitive data exposed
- ✅ HTTPS ready

## 📊 API Endpoints

```
POST /api/register          - Create account
POST /api/login             - Login
POST /api/logout            - Logout
GET  /api/user              - Get user info
POST /api/chat              - Send message
GET  /api/chat-history      - Get past messages
GET  /api/recent-chats      - Get recent chats
GET  /api/subscription      - Get subscription info
POST /api/upgrade           - Upgrade subscription
POST /api/export            - Export chat
```

## 🌐 Deploy Right Now (Choose One)

### Option 1: Railway.app (Easiest)
```
1. Go to https://railway.app
2. Click "Deploy on Railway"
3. Connect GitHub
4. Add environment variables
5. Done! ✅
```

### Option 2: Render.com
```
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub
4. Add environment variables
5. Deploy ✅
```

### Option 3: Heroku
```
# Install Heroku CLI
heroku login
heroku create your-jarvis-app
heroku config:set OPENROUTER_API_KEY="your_key"
git push heroku main
✅
```

## 💻 Environment Variables

Create `.env` file or set in your deployment platform:

```
OPENROUTER_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
PORT=5000
```

## 📱 Mobile Friendly

The web app is fully responsive:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones
- ✅ Touch-friendly buttons
- ✅ Works offline (local data)

## 🎨 Customization

### Change Colors:
Edit in `templates/index.html` (search for `#10a37f` - main green color)

### Add Features:
1. Modify `app.py` (backend)
2. Modify `templates/index.html` (frontend)
3. Update `database.py` for new data

## 🐛 Troubleshooting

### App doesn't start
```bash
pip install -r requirements-web.txt
python app.py
```

### API key not working
- Get key from https://openrouter.ai
- Set it in environment variables
- Restart app

### Database errors
- Database auto-creates on first run
- Check folder permissions
- Delete `jarvis_data.db` to reset

### Can't access from phone
- Make sure you're on same WiFi (local)
- Or use deployed live URL
- Check firewall settings

## 📈 Usage Analytics

The app tracks:
- Users registered
- Messages sent
- Queries per tier
- Subscription upgrades
- Chat history

## 🔄 Updates

To update the app:
```bash
git pull
pip install -r requirements-web.txt
# If deployed: git push to your platform
```

## 💡 Pro Tips

1. **For Production:**
   - Use strong SECRET_KEY
   - Enable HTTPS
   - Set up backups
   - Enable monitoring

2. **For Scaling:**
   - Use PostgreSQL instead of SQLite
   - Add Redis for sessions
   - Use load balancer
   - CDN for static files

3. **For Users:**
   - Create custom domain
   - Add email verification
   - Set up password reset
   - Add 2FA option

## 🤝 Contributing

Want to improve Jarvis?
1. Fork the repo
2. Make changes
3. Test locally
4. Submit pull request

## 📞 Support

- 📧 Email: support@jarvis.ai (placeholder)
- 🐛 Issues: GitHub Issues
- 💬 Chat: In-app support

## 📜 License

MIT License - Feel free to use and modify

## 🎉 You're All Set!

Your Jarvis AI Assistant is ready for the world! 

**Next Steps:**
1. ✅ Test locally (run start.bat)
2. ✅ Get OPENROUTER_API_KEY
3. ✅ Deploy to Railway/Render/Heroku
4. ✅ Share your link!
5. ✅ Get users to sign up
6. ✅ Enjoy real-time interactions

---

Made with ❤️ by the Jarvis Team
