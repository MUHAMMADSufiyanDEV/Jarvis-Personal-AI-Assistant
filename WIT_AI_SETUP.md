# Jarvis AI Assistant - Wit.ai Integration Guide

## 🎯 Overview

Jarvis now supports **Wit.ai** as the primary AI service! Wit.ai provides excellent natural language understanding capabilities.

---

## 📋 Getting Your Wit.ai API Key

### Step 1: Create a Wit.ai Account
- Go to https://wit.ai
- Click **"Sign up"** or **"Sign in"** with your account
- Complete the signup process

### Step 2: Create a New App
- Once logged in, go to **Dashboard**
- Click **"Create new app"**
- Name it `Jarvis` or something memorable
- Select your language (English)
- Click **"Create"**

### Step 3: Get Your API Key
- In your app dashboard, click **"Settings"** or go to **Management → Settings**
- Look for **"API Details"** or **"Server Access Token"**
- Copy the **Server Access Token** (starts with `API_` or similar)
- This is your `WIT_AI_API_KEY`

### Step 4: Configure Jarvis

**Option A: Environment Variable (Recommended)**
```powershell
# Windows
set WIT_AI_API_KEY=YOUR_API_KEY_HERE
python main.py

# Mac/Linux
export WIT_AI_API_KEY=YOUR_API_KEY_HERE
python main.py
```

**Option B: .env File**
1. Open `.env.example` file in the jarvis folder
2. Replace `YOUR_WIT_AI_API_KEY_HERE` with your actual API key
3. Save as `.env` (without the `.example`)
4. Run: `python main.py`

---

## ✨ How Wit.ai Integration Works

### Intent Recognition
Wit.ai automatically recognizes what the user is trying to do:
- **Greetings**: "Hello", "Hi", "How are you?"
- **Questions**: "What time is it?", "What's the date?"
- **Commands**: "Open notepad", "Close this"
- **General Chat**: Any other message

### Entity Extraction
Wit.ai extracts important information:
- **People**: Names mentioned
- **Locations**: Places
- **Dates/Times**: When something should happen
- **Numbers**: Quantities, amounts

### Smart Responses
Jarvis generates contextual responses based on:
- Detected intent
- Extracted entities
- Your previous messages
- Time-based context

---

## 🚀 Deployment

### Deploy to Heroku with app.json
```bash
# 1. Push code to GitHub
git push origin main

# 2. Go to Heroku
# 3. Create new app
# 4. Connect to GitHub repo
# 5. Enable "Deploy from GitHub"
# 6. Or use this button (add to README):
# Deploy via app.json with one click
```

### Deploy to Railway
```bash
# 1. Go to https://railway.app
# 2. Create new project
# 3. Connect GitHub repo
# 4. Set environment variable:
#    WIT_AI_API_KEY=YOUR_KEY
# 5. Deploy!
```

---

## 🧪 Testing

### Test Locally
```bash
python main.py
```

### Test Voice Recognition
1. Click 🎤 button
2. Say a phrase like:
   - "What time is it?"
   - "Open notepad"
   - "How are you?"
3. Jarvis should respond with voice

### Test Chat
1. Type a message in the chat box
2. Jarvis will use Wit.ai to understand
3. Response will be spoken and displayed

---

## 📊 Training Your Wit.ai App

### Improve Recognition
1. Go to your Wit.ai app dashboard
2. Review **"Inbox"** for misunderstood phrases
3. Mark what the user meant
4. Wit.ai learns from your feedback

### Add Custom Intents
1. In **"Intents"** section, create new intent
2. Name it (e.g., "device_control")
3. Add example phrases
4. Wit.ai will recognize similar phrases

### Manage Entities
1. In **"Entities"** section, define custom entities
2. Add values and synonyms
3. Wit.ai uses these to extract information

---

## 🔄 Fallback to OpenRouter

If Wit.ai is not configured, Jarvis automatically falls back to OpenRouter:
```python
WIT_AI_API_KEY=  # Empty
OPENROUTER_API_KEY=your_key  # Set this

# Result: Uses OpenRouter instead
```

---

## 🆘 Troubleshooting

### "No AI API configured"
- Set `WIT_AI_API_KEY` environment variable
- Or create `.env` file with key
- Restart app

### "Wit.ai API Key issue"
- Verify key is correct
- Check it's a Server Access Token (not Client Token)
- Go to wit.ai and generate a new token

### "Rate limited"
- Wit.ai free tier has limits
- Wait a moment before retrying
- Consider upgrading plan

### "No internet connection"
- Check your network
- Verify wit.ai is accessible
- Check firewall settings

---

## 📚 Resources

- **Wit.ai Docs**: https://wit.ai/docs
- **Wit.ai API Reference**: https://wit.ai/docs/http/20170307
- **Best Practices**: https://wit.ai/docs/recipes
- **Example Apps**: https://wit.ai/docs/tutorials

---

## 💡 Tips

1. **Short phrases work better** for voice recognition
2. **Natural language is better** than commands
3. **Train your app** by reviewing inbox
4. **Use custom intents** for specific tasks
5. **Test in console** before deploying

---

## 📝 Example Interactions

### Example 1: Greeting
```
User: "Hey, how are you?"
Wit.ai Intent: greeting
Response: "Hello! How can I assist you today?"
```

### Example 2: Time Query
```
User: "What's the time?"
Wit.ai Intent: time
Response: "The current time is 3:45 PM"
```

### Example 3: Device Control
```
User: "Open notepad"
Wit.ai Intent: device_control
Response: "Opening notepad..."
```

---

## ✅ You're All Set!

Your Jarvis is now ready to use Wit.ai! 🎉

Enjoy your AI assistant with natural language understanding! 🚀
