# 🎬 Getting Started Guide - Jarvis 2.0

## Welcome! 👋

This guide will walk you through using Jarvis 2.0 step-by-step.

## Step 1: Launch Jarvis

### How to Start
```bash
# Navigate to jarvis folder
cd "c:\Users\REHMAN COMPUTER\Downloads\jarvis"

# Run the application
python main.py
```

### What You'll See
```
┌─────────────────────────────────┐
│  🤖 JARVIS                      │
│  AI Assistant                   │
│                                 │
│  [Username input field]         │
│  [Password input field]         │
│                                 │
│  [Login]  [Create New Account]  │
│  [Continue as Guest]            │
└─────────────────────────────────┘
```

---

## Step 2: Choose Your Path

### Option A: Create New Account (First Time)

**Click**: "Create New Account"

```
Screen: Registration
┌─────────────────────────────────┐
│  Register                       │
│                                 │
│  Username: [_____________]      │
│  Email: [_________________]     │
│  Password: [______________]     │
│  Confirm: [______________]      │
│                                 │
│  [Register]  [Back to Login]    │
└─────────────────────────────────┘
```

**Fill in**:
- Username (min 3 characters)
- Email (must be valid)
- Password (min 6 characters)
- Confirm password

**Click**: "Register"

**You'll see**: "Account created successfully!"

---

### Option B: Login Existing Account

**Enter**:
- Username
- Password

**Click**: "Login"

**You'll see**: Welcome message with your username

---

### Option C: Guest Mode

**Click**: "Continue as Guest"

**Note**: Conversations won't be saved

---

## Step 3: Main Jarvis Window

### What You'll See

```
┌─────────────────────────────────────────────────┐
│ 🤖 JARVIS - AI Assistant                        │
│ ✅ AI Enabled | 👤 username | Tier: FREE       │
├─────────────────────────────────────────────────┤
│                                                  │
│  [Chat Display Area]                            │
│  [Welcome message appears here]                 │
│  [Your messages appear here]                    │
│  [AI responses appear here]                     │
│  [Auto-scrolls to show latest]                  │
│                                                  │
├─────────────────────────────────────────────────┤
│  [Input field: Type your question here.....] │
│  [📤 Send] [🎤 Listen] [🗑️ Clear] [☰ Menu]   │
└─────────────────────────────────────────────────┘
```

### Components

**Header Section**
- Shows your username (if logged in)
- Shows subscription tier
- Shows AI status
- Shows query count for free users

**Chat Area**
- Displays conversation history
- Shows timestamps
- Color-coded messages (user/AI)
- Auto-scrolls

**Input Area**
- Type your question
- Press Enter to send

**Buttons**
- 📤 **Send** - Send text message
- 🎤 **Listen** - Use voice input
- 🗑️ **Clear** - Clear chat
- ☰ **Menu** - Access features

---

## Step 4: Using Basic Features

### Typing a Message

```
1. Click in the input field
2. Type your question
   Example: "What is Python?"
3. Press Enter
   OR
   Click "📤 Send" button
```

### Using Voice Input

```
1. Click "🎤 Listen" button
2. You'll see: "🎤 Listening... (5 seconds)"
3. Speak your question clearly
4. Wait for AI response
```

### Clearing Chat

```
1. Click "🗑️ Clear" button
2. Current chat clears (history saved if logged in)
3. Ready for new conversation
```

---

## Step 5: Using the Menu (☰)

### Click Menu Button

```
┌──────────────────────────┐
│  ☰ Menu                  │
├──────────────────────────┤
│  💎 Subscriptions        │
│  📜 Chat History         │
│  👤 Account Info         │
│  🚪 Logout               │
└──────────────────────────┘
```

### Feature 1: View Subscriptions

**Click**: "💎 Subscriptions"

```
Subscription Plans
┌─────────────────────────────────────────┐
│  📦 FREE              🔹 PRO           💎 PREMIUM
│                                         
│  $0/month            $9.99/month       $19.99/month
│                                         
│  ✓ 100 queries      ✓ 1000 queries    ✓ 10000 queries
│  ✓ Voice input      ✓ Priority voice  ✓ Priority voice
│  ✓ Chat history     ✓ Unlimited hist. ✓ Unlimited hist.
│  ✓ Basic support    ✓ Ad-free         ✓ Ad-free
│                     ✓ Priority supp.  ✓ 24/7 Premium
│                                         
│  [Current]          [Upgrade]         [Upgrade]
└─────────────────────────────────────────┘
```

**To Upgrade**:
1. Click "Upgrade" on your desired tier
2. Your subscription changes immediately
3. You'll see confirmation message

---

### Feature 2: View Chat History

**Click**: "📜 Chat History"

```
Chat History
┌────────────────────────────────────┐
│  📜 Chat History                   │
│  Total: 15 chats | Today: 3 chats  │
│                                    │
│  [15:30:45] You: Hello!            │
│  Jarvis: Hi there! How can I help? │
│                                    │
│  [15:31:02] You: What time is it?  │
│  Jarvis: The current time is...    │
│                                    │
│  [15:32:15] You: How does AI work? │
│  Jarvis: AI works by using neural  │
│  networks to process information...│
│                                    │
└────────────────────────────────────┘
```

**In Chat History**:
- See all past conversations
- Timestamps for each message
- View statistics (total chats, today's chats)
- Scroll through history
- Reference past conversations

---

### Feature 3: Account Information

**Click**: "👤 Account Info"

```
Account Information
┌────────────────────────────────┐
│  👤 Username: john_doe         │
│  📧 Email: john@example.com    │
│  💎 Subscription: FREE         │
│                                │
│  📊 Statistics:                │
│  ├─ Total Chats: 15           │
│  ├─ Today's Chats: 3          │
│  ├─ Queries Used: 45/100      │
│  └─ Joined: 2026-01-15        │
│                                │
│  ✨ Features:                  │
│  ├─ Voice Enabled: Yes         │
│  ├─ Ad-Free: No               │
│  └─ Priority Support: No       │
└────────────────────────────────┘
```

**Information Shows**:
- Your username
- Your email
- Current subscription tier
- Total conversations
- Today's conversations
- Queries used vs limit
- Account creation date
- Features available

---

### Feature 4: Logout

**Click**: "🚪 Logout"

```
You'll see: "You have been logged out successfully"
The application closes
```

**To Log Back In**:
```bash
python main.py
# Enter your username and password again
```

---

## Full Workflow Example

### Scenario: Free Tier User's First Day

```
1. Launch Application
   └─ python main.py

2. Create Account
   └─ Register with email

3. Welcome Screen
   └─ See greeting with username

4. Ask a Question
   └─ "What is machine learning?"
   └─ Get AI response
   └─ 1/100 queries used

5. Ask Another Question
   └─ "Explain neural networks"
   └─ Get response
   └─ 2/100 queries used

6. Check Progress
   └─ Menu → Account Info
   └─ See 2 queries used
   └─ 98 remaining this month

7. View History
   └─ Menu → Chat History
   └─ See both conversations
   └─ See timestamps

8. Explore Subscriptions
   └─ Menu → Subscriptions
   └─ See Pro plan ($9.99)
   └─ See Premium plan ($19.99)

9. Continue Chatting
   └─ Ask more questions
   └─ Track query count

10. Logout
    └─ Menu → Logout
    └─ See confirmation
```

---

## Common Tasks

### Task 1: Save a Conversation

✅ **Automatic**! Every message is saved when you're logged in.

```
1. Login to account
2. Chat normally
3. Close application
4. Reopen and login
5. Click Menu → Chat History
6. Your conversation is there!
```

### Task 2: Use Voice Instead of Typing

```
1. Click "🎤 Listen" button
2. Wait for "Listening..." message
3. Speak clearly
4. Wait 5 seconds
5. AI processes and responds
```

### Task 3: Switch Subscription Tier

```
1. Click "☰ Menu"
2. Click "💎 Subscriptions"
3. Click "Upgrade" on desired plan
4. See confirmation
5. New tier active immediately!
```

### Task 4: Find Old Conversation

```
1. Click "☰ Menu"
2. Click "📜 Chat History"
3. Scroll through history
4. Find your conversation
5. Read past messages
```

### Task 5: Check Query Remaining

```
1. Click "☰ Menu"
2. Click "👤 Account Info"
3. Look for "Queries Used: X/100"
4. Calculate remaining
5. OR upgrade for more queries
```

---

## Tips & Tricks

### 💡 Productivity Tips

**Organize Your Thoughts**
```
Instead of: "Tell me everything about Python"
Try: "What are the top 5 Python data structures?"
More specific = Better responses
```

**Use History for Reference**
```
1. Ask a question
2. Save the response
3. Refer back later via history
4. No need to re-ask!
```

**Upgrade When Needed**
```
Free users get ~3 queries/day
Pro users get ~33 queries/day
Upgrade when you need more!
```

### ⚡ Voice Tips

**Clear Speech Works Best**
- Speak normally
- Avoid background noise
- Wait for listening to start
- Speak during the 5 seconds

**When Voice Doesn't Work**
- Try typing instead
- Check microphone connection
- Check Windows audio settings
- Restart and try again

### 🔄 History Tips

**Track Your Learning**
- Browse past conversations
- Review questions you asked
- See how your thinking evolved
- Reference solutions

**Manage Storage**
- Each chat takes ~1KB
- 1,000 chats = ~1MB
- Very efficient storage!
- No cleanup needed

---

## Your First Questions

### Great First Questions to Ask

✅ "What is artificial intelligence?"  
✅ "How do I learn Python?"  
✅ "Explain photosynthesis"  
✅ "What's the capital of France?"  
✅ "Write a simple Python function"  
✅ "How does the internet work?"  

### Pro Tips

- Be specific in questions
- You can ask follow-ups
- Voice input for hands-free
- History keeps your progress

---

## Troubleshooting

### "I forgot my password"
```
Solution: Create a new account
The app doesn't have password recovery yet
You can use a different email or use Guest mode
```

### "My chat isn't saving"
```
Solution: Make sure you're logged in
Guest mode doesn't save chats
Check the header to see your username
```

### "I reached my query limit"
```
Solution: Upgrade to Pro or Premium tier
Free tier resets monthly
Check Account Info for exact count
```

### "Voice input isn't working"
```
Solution: Check these:
1. Microphone is connected
2. Windows audio settings enabled
3. Microphone is not muted
4. Try typing instead (still works!)
```

---

## Next Steps

### What to Try Now

1. ✅ Create an account
2. ✅ Ask your first question
3. ✅ Use voice input
4. ✅ Check chat history
5. ✅ View account info
6. ✅ Explore subscriptions

### Further Reading

- **NEW_FEATURES.md** - Detailed features
- **README_2.0.md** - Full overview
- **QUICK_START.md** - Quick reference

---

## Enjoy Jarvis 2.0! 🚀

You're now ready to use all the amazing features!

```bash
# Get started:
python main.py
```

**Questions?** Check the documentation!  
**Issues?** Review troubleshooting section!  
**Need more?** Upgrade to Pro or Premium!

---

**Happy chatting!** 💬  
**Version**: 2.0  
**Date**: January 2026
