# 🤖 Jarvis Device Control - Complete Guide

## 🎯 Full Device Control Features

Jarvis can now control your entire device! Here's everything you can do:

---

## 📱 Application Control

### Open Applications
```
"Open notepad"
"Open calculator"
"Open chrome"
"Open discord"
"Open spotify"
"Open vlc"
"Open vscode"
"Open paint"
"Open word"
"Open excel"
```

**Supported Applications:**
- Notepad
- Calculator
- Paint
- Microsoft Word
- Microsoft Excel
- PowerPoint
- Chrome
- Firefox
- Discord
- Spotify
- VLC Media Player
- Blender
- VS Code
- Visual Studio
- GIMP
- Photoshop

### Close Applications
```
"Close chrome"
"Close notepad"
"Close spotify"
"Close [any app]"
```

---

## 🔊 System Control

### Volume Control
```
"Volume up"
"Volume down"
"Mute"
```

### Brightness Control
```
"Brightness up"
"Brightness down"
"Increase brightness"
"Decrease brightness"
```

### System Power
```
"Shutdown"
"Restart"
"Reboot"
"Put system to sleep"
"Hibernation"
"Lock system"
"Lock"
```

---

## 💬 Messaging Features

### WhatsApp
```
"Send whatsapp message"
```
Note: Opens WhatsApp Web. You need to be logged in.

### Instagram
```
"Send instagram message"
```
Note: Opens Instagram. Requires web browser automation.

---

## 🔍 Web Search & Browsing

```
"Search python tutorials"
"Search machine learning"
"Open google"
"Open youtube"
"Wikipedia quantum computing"
```

---

## ⏰ Information

```
"What time is it?"
"What's the date?"
"Tell me the time"
"Current date"
```

---

## 🤖 AI Queries

Ask anything and Jarvis will use AI to answer:
```
"What is machine learning?"
"How do I learn Python?"
"Explain quantum computing"
"Write a hello world program"
"What's the capital of France?"
"Tell me a joke"
"How do I make pasta?"
```

---

## 🎤 Usage Methods

### Method 1: Type Commands
1. Type your command in the text field
2. Press **Enter** or click **Send**
3. Jarvis will execute and respond

### Method 2: Voice Commands
1. Click **🎤 Listen**
2. Speak your command clearly (5 seconds)
3. Jarvis will process and execute

### Method 3: Hybrid
Type or speak - Jarvis understands both!

---

## ⚙️ Advanced Configuration

### Setting OpenRouter API Key
Required for advanced AI answers.

**Option 1: Temporary (Current session only)**
```powershell
$env:OPENROUTER_API_KEY="your_api_key"
python main.py
```

**Option 2: Permanent (Windows)**
1. Press `Win + X` → "System"
2. "Advanced system settings"
3. "Environment Variables" → "New"
4. Name: `OPENROUTER_API_KEY`
5. Value: `your_api_key`
6. Restart terminal

---

## 🚀 Example Workflows

### Workflow 1: Morning Routine
```
"What time is it?"
"Open spotify"
"What's the weather?" (AI will answer)
"Open chrome"
```

### Workflow 2: Development
```
"Open vscode"
"Open notepad"
"Search python documentation"
"What is a decorator in Python?" (AI answer)
```

### Workflow 3: Entertainment
```
"Open youtube"
"Search meme compilation"
"Open spotify"
"Volume up"
```

---

## ⚠️ Important Notes

### Device Control Permissions
- Some features require administrator privileges
- Run as Administrator for full system control
- WhatsApp/Instagram messaging works via web automation

### Security
- Never share your API key
- Jarvis stores no personal data
- All processing happens locally or through OpenRouter

### Best Practices
- Speak clearly for voice commands
- Use complete app names for reliability
- Report bugs or unexpected behavior

---

## 🔧 Troubleshooting

### App Won't Open
- Check if app is installed
- Try using full path: "Open C:\\Program Files\\AppName"
- Restart Jarvis

### Voice Commands Not Working
- Check microphone is connected
- Ensure no background noise
- Speak clearly and wait for "Listening" message

### System Commands Require Admin
- Right-click terminal → "Run as Administrator"
- Or: `runas /user:Administrator "python main.py"`

### WhatsApp Not Sending
- Must be manually logged in to WhatsApp Web first
- Browser must stay open during send
- Some security features may block automation

---

## 📊 Command Reference Table

| Command | Purpose | Example |
|---------|---------|---------|
| Open [app] | Launch application | "Open notepad" |
| Close [app] | Close application | "Close chrome" |
| Volume [up/down] | Adjust volume | "Volume up" |
| Mute | Silence system | "Mute" |
| Brightness [up/down] | Adjust display | "Brightness down" |
| Lock | Lock system | "Lock system" |
| Shutdown | Turn off PC | "Shutdown" |
| Restart | Reboot PC | "Restart" |
| Search [query] | Google search | "Search AI" |
| Time | Current time | "What time is it?" |
| Date | Current date | "What's the date?" |
| [Any question] | AI answer | "What is AI?" |

---

## 🎓 Learning Resources

- [OpenRouter AI](https://openrouter.ai)
- [Python Documentation](https://python.org/docs)
- [Vosk Speech Recognition](https://alphacephei.com/vosk)

---

## 📞 Support

For issues or feature requests, check:
1. Terminal output for error messages
2. Troubleshooting section above
3. Ensure Python and all packages are updated

---

**Enjoy your fully-featured Jarvis AI Assistant!** 🚀🤖
