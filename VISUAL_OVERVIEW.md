# 🎨 Jarvis 2.0 - Visual Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   JARVIS 2.0 ARCHITECTURE               │
└─────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   main.py        │ ← Entry point
                    │  (Tkinter UI)    │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
    ┌────────────┐    ┌─────────────┐    ┌──────────────┐
    │  database  │    │   account   │    │   auth_ui    │
    │    .py     │    │  _manager   │    │     .py      │
    │            │    │    .py      │    │              │
    │ • Users    │    │             │    │ • Login      │
    │ • History  │    │ • Register  │    │ • Register   │
    │ • Sessions │    │ • Auth      │    │ • Subs View  │
    │ • Subs     │    │ • Tiers     │    │ • History    │
    └────────────┘    └─────────────┘    └──────────────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │  jarvis_data.db  │ ← SQLite
                    │   (Database)     │
                    │                  │
                    │ • Users table    │
                    │ • History table  │
                    │ • Subs table     │
                    │ • Sessions table │
                    └──────────────────┘
```

## Data Flow

```
USER LAUNCHES APP
        │
        ▼
┌──────────────────┐
│ Authentication   │
│   Window         │
└──────────────────┘
    │     │     │
    ▼     ▼     ▼
┌─────┐ ┌──────┐ ┌─────────┐
│Login│ │Register│ │Guest    │
└─────┘ └──────┘ └─────────┘
    │        │         │
    └────┬───┴─────┬───┘
         │         │
         ▼         ▼
    ┌─────────────────┐
    │ Main Chat Window│
    │ (Personalized)  │
    └─────────────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    │          │          │          │
    ▼          ▼          ▼          ▼
┌────────┐┌────────┐┌─────────┐┌──────────┐
│Chat    ││Voice   ││View     ││Menu      │
│Input   ││Input   ││History  ││Options   │
└────────┘└────────┘└─────────┘└──────────┘
    │
    ├─→ Check Query Limit
    │
    ├─→ Send to AI
    │
    ├─→ Auto-Save to History
    │
    └─→ Display Response
```

## Feature Map

```
JARVIS 2.0
│
├─ 🔐 ACCOUNT SYSTEM
│  ├─ User Registration
│  ├─ Login/Logout
│  ├─ Password Hashing
│  ├─ Guest Mode
│  └─ Session Management
│
├─ 💎 SUBSCRIPTIONS
│  ├─ Free Tier (100/month)
│  ├─ Pro Tier ($9.99/month)
│  ├─ Premium Tier ($19.99/month)
│  ├─ Query Limits
│  └─ Tier Upgrades
│
├─ 📜 CHAT HISTORY
│  ├─ Auto-Save
│  ├─ Browse History
│  ├─ Session Tracking
│  ├─ Timestamps
│  └─ Statistics
│
├─ 👤 USER PROFILE
│  ├─ Account Info
│  ├─ Usage Stats
│  ├─ Query Count
│  └─ Feature Display
│
├─ 🎨 USER INTERFACE
│  ├─ Auth Screen
│  ├─ Chat Window
│  ├─ Menu System
│  ├─ Subscriptions View
│  └─ History Browser
│
└─ 🗄️ DATABASE
   ├─ Users (9 columns)
   ├─ Chat History (6 columns)
   ├─ Subscriptions (12 columns)
   └─ Sessions (6 columns)
```

## UI Flow Diagram

```
START
  │
  ▼
┌─────────────────┐
│ Login Window    │
│ (Auth Screen)   │
└────────┬────────┘
    │    │    │
    │    │    └──→ Guest
    │    │        (No save)
    │    │
    │    └──→ Register
    │        │
    │        ▼
    │     Create
    │     Account
    │        │
    │        ▼
    │     Login
    │
    └──→ Login
         │
         ▼
    ┌─────────────┐
    │ Main Window │ ← Personalized
    │ Chat Area   │
    └──────┬──────┘
           │
           ├─→ [📤 Send]    ← Text input
           │
           ├─→ [🎤 Listen]  ← Voice input
           │
           ├─→ [🗑️ Clear]   ← Clear chat
           │
           └─→ [☰ Menu]    ← Open menu
                │
                ├─→ [💎 Subscriptions]
                │   └─→ View plans
                │   └─→ Upgrade
                │
                ├─→ [📜 Chat History]
                │   └─→ Browse all chats
                │
                ├─→ [👤 Account Info]
                │   └─→ View profile
                │
                └─→ [🚪 Logout]
                    └─→ Sign out
```

## Database Schema (Visual)

```
USERS TABLE
┌──────────────────────────────────┐
│ id (PK)                          │
│ username (UNIQUE)                │
│ password (hashed)                │
│ email (UNIQUE)                   │
│ subscription_tier (free/pro/pre) │
│ created_at                       │
│ last_login                       │
│ queries_used                     │
│ max_queries                      │
└──────────────────────────────────┘
           │
           │ (1:N relationship)
           │
           ├──→ CHAT_HISTORY TABLE
           │    ┌─────────────────────┐
           │    │ id (PK)             │
           │    │ user_id (FK)        │
           │    │ query               │
           │    │ response            │
           │    │ timestamp           │
           │    │ session_id          │
           │    └─────────────────────┘
           │
           ├──→ SUBSCRIPTIONS TABLE
           │    ┌─────────────────────┐
           │    │ id (PK)             │
           │    │ user_id (FK)        │
           │    │ tier                │
           │    │ max_queries         │
           │    │ voice_enabled       │
           │    │ ad_free             │
           │    │ priority_support    │
           │    │ start_date          │
           │    │ end_date            │
           │    └─────────────────────┘
           │
           └──→ SESSIONS TABLE
                ┌─────────────────────┐
                │ id (PK)             │
                │ user_id (FK)        │
                │ session_id (UNIQUE) │
                │ created_at          │
                │ last_active         │
                │ is_active           │
                └─────────────────────┘
```

## Subscription Tier Comparison

```
┌──────────────────────────────────────────────────┐
│ SUBSCRIPTION TIERS                               │
├──────────────────────────────────────────────────┤
│                                                  │
│ FREE          │ PRO           │ PREMIUM          │
│ ─────────────┼───────────────┼──────────────    │
│              │               │                  │
│ $0/month      │ $9.99/month   │ $19.99/month     │
│              │               │                  │
│ ✓ 100/month  │ ✓ 1000/month │ ✓ 10000/month    │
│ ✓ Voice      │ ✓ Voice pri. │ ✓ Voice pri.     │
│ ✓ 7d hist   │ ✓ Unlimited  │ ✓ Unlimited      │
│ ✓ Basic sup  │ ✓ Ad-free    │ ✓ Ad-free        │
│ ✗ Ad-free    │ ✓ Priority   │ ✓ 24/7 Support   │
│ ✗ Priority   │ ✓ Advanced   │ ✓ All features   │
│ ✗ 24/7 sup   │ ✗ 24/7 sup   │ ✓ Early access   │
│              │               │                  │
└──────────────────────────────────────────────────┘
```

## File Structure (Tree View)

```
jarvis/
│
├── Python Files (New)
│   ├── database.py               (280 lines)
│   ├── account_manager.py        (160 lines)
│   └── auth_ui.py               (420 lines)
│
├── Python Files (Updated)
│   └── main.py                  (+100 lines)
│
├── Data Files (Auto-created)
│   └── jarvis_data.db           (SQLite)
│
├── Documentation (New)
│   ├── START_HERE.md            ← Read this first!
│   ├── GETTING_STARTED.md
│   ├── QUICK_START.md
│   ├── NEW_FEATURES.md
│   ├── README_2.0.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   ├── FEATURE_CHECKLIST.md
│   ├── PACKAGE_SUMMARY.md
│   └── DOCUMENTATION_INDEX.md
│
├── Model & Config
│   ├── vosk-model-small-en-us-0.15/
│   ├── requirements.txt
│   └── SETUP_OPENROUTER.md
│
└── Other Files
    └── [Original files unchanged]
```

## User Journey

```
1. FIRST TIME USER
   │
   ├─ Download/Install
   ├─ Read: START_HERE.md
   ├─ Run: python main.py
   ├─ Click: "Create New Account"
   ├─ Fill: Username, Email, Password
   ├─ Confirm: Registration successful
   ├─ Login: With credentials
   ├─ Welcome: Personalized greeting
   └─ Start: Using Jarvis!

2. DAILY USER (Free Tier)
   │
   ├─ Run: python main.py
   ├─ Login: With credentials
   ├─ Ask: Questions (~3/day average)
   ├─ View: Chat history anytime
   ├─ Track: Queries remaining
   └─ Save: All conversations

3. PRO USER (Paid Tier)
   │
   ├─ Upgrade: From free tier
   ├─ Enjoy: 1000 queries/month
   ├─ Access: Priority features
   ├─ Get: Ad-free experience
   └─ Save: Unlimited history

4. POWER USER (Premium Tier)
   │
   ├─ Upgrade: From any tier
   ├─ Unlimited: 10000 queries/month
   ├─ Support: 24/7 priority help
   ├─ Access: All features
   └─ Enjoy: Early access to new features
```

## Authentication Flow

```
┌──────────────┐
│ App Starts   │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Auth Window Opens    │
│ (Before Main Window) │
└──┬────────┬──────┬───┘
   │        │      │
   ▼        ▼      ▼
┌──────┐ ┌──────┐ ┌─────────┐
│Login │ │Regis │ │Guest    │
│Form  │ │Form  │ │Mode     │
└──┬───┘ └──┬───┘ └─────┬───┘
   │        │          │
   ▼        ▼          ▼
┌─────────────────────────┐
│ Validation              │
│ ├─ Check credentials    │
│ ├─ Hash password        │
│ └─ Create session       │
└───────┬─────────────────┘
        │
        ▼
┌──────────────────┐
│ Main Window      │
│ (Personalized)   │
│ or Guest Mode    │
└──────────────────┘
```

## Processing Flow

```
USER INPUT
    │
    ├─→ Text Input (Type)
    │   └─→ Press Enter
    │
    └─→ Voice Input (Speak)
        └─→ 5 second recording
    
    │
    ▼
VALIDATION
    ├─→ Check login status
    ├─→ Check query limit
    └─→ Validate input
    
    │
    ▼
PROCESSING
    ├─→ Route to command handler OR AI
    ├─→ Execute action
    └─→ Generate response
    
    │
    ▼
STORAGE
    ├─→ Save query
    ├─→ Save response
    ├─→ Increment counter
    └─→ Update timestamp
    
    │
    ▼
OUTPUT
    ├─→ Display in chat
    ├─→ Speak aloud (if enabled)
    └─→ Store in history
```

## Security Architecture

```
USER PASSWORD
    │
    ▼ SHA-256 Hashing
    │
HASHED PASSWORD (never plain text)
    │
    ▼ Store in Database
    │
ENCRYPTED DATABASE FILE
    │
    ├─→ Local storage only
    ├─→ User-specific encryption
    ├─→ Session tokens
    └─→ Auto-logout on exit
```

## Module Dependencies

```
main.py
├── Imports: database.py
├── Imports: account_manager.py
├── Imports: auth_ui.py
│
account_manager.py
├── Imports: database.py
├── Uses: hashlib (encryption)
└── Uses: uuid (sessions)

auth_ui.py
├── Imports: account_manager.py
└── Imports: database.py

database.py
└── Uses: sqlite3 (database)
```

## Quick Reference Matrix

```
┌────────────┬──────────────┬───────────────┬──────────────┐
│ Feature    │ Free         │ Pro           │ Premium      │
├────────────┼──────────────┼───────────────┼──────────────┤
│ Queries    │ 100/month    │ 1000/month    │ 10000/month  │
│ Cost       │ $0           │ $9.99/month   │ $19.99/month │
│ History    │ 7 days       │ Unlimited     │ Unlimited    │
│ Voice      │ Yes          │ Priority      │ Priority     │
│ Ad-free    │ No           │ Yes           │ Yes          │
│ Support    │ Basic        │ Priority      │ 24/7 Premium │
│ Features   │ Basic        │ Advanced      │ All          │
│ Access     │ Current      │ Upgrade       │ Upgrade      │
└────────────┴──────────────┴───────────────┴──────────────┘
```

---

**Created**: January 2026  
**Version**: 2.0  
**Status**: ✅ Complete
