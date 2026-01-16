# 🤖 Jarvis - New Features Guide

## Overview

Jarvis has been upgraded with professional account management, subscription tiers, and persistent chat history - similar to ChatGPT!

## New Core Features

### 1. 🔐 User Account System
- **Registration**: Create a new account with username, email, and password
- **Login**: Secure login with authentication
- **Guest Mode**: Continue as guest without creating an account
- **Persistent Data**: All user data is saved in a local SQLite database

### 2. 💎 Subscription Tiers

#### Free Tier ($0/month)
- ✓ 100 queries/month
- ✓ Voice input enabled
- ✓ Chat history (last 7 days)
- ✓ Basic support

#### Pro Tier ($9.99/month)
- ✓ 1000 queries/month
- ✓ Priority voice processing
- ✓ Unlimited chat history
- ✓ Priority support
- ✓ Ad-free experience
- ✓ Advanced features

#### Premium Tier ($19.99/month)
- ✓ 10,000 queries/month
- ✓ Priority voice processing
- ✓ Unlimited chat history
- ✓ 24/7 Premium support
- ✓ Ad-free experience
- ✓ All advanced features
- ✓ Custom settings
- ✓ Early access to new features

### 3. 📜 Chat History
- **Save All Conversations**: Every conversation is automatically saved
- **View History**: Browse past conversations anytime
- **Search**: Find specific conversations (coming soon)
- **Sessions**: Organized by conversation sessions
- **Statistics**: Track total chats and daily usage

### 4. 👤 User Profile
- **Account Information**: View username, email, subscription tier
- **Usage Statistics**: See total chats and today's usage
- **Query Tracking**: Monitor remaining queries for free tier users
- **Join Date**: See when your account was created

## How to Use

### Getting Started

1. **First Launch**
   ```
   python main.py
   ```

2. **Authentication Screen**
   - Choose one of three options:
     - **Login**: Enter existing credentials
     - **Create New Account**: Register with email and password
     - **Continue as Guest**: Use without saving data

### Creating an Account

1. Click "Create New Account"
2. Enter:
   - **Username** (min 3 characters)
   - **Email** (valid email format)
   - **Password** (min 6 characters)
   - **Confirm Password**
3. Click "Register"
4. Login with your new credentials

### Using Subscriptions

1. Click "☰ Menu" button
2. Click "💎 Subscriptions"
3. View available plans
4. Click "Upgrade" on desired plan
5. Plan changes take effect immediately

### Viewing Chat History

1. Login to your account
2. Click "☰ Menu" button
3. Click "📜 Chat History"
4. Browse all your past conversations
5. See timestamps and statistics

### Managing Your Account

1. Click "☰ Menu" button
2. Click "👤 Account Info" to see:
   - Username and email
   - Current subscription tier
   - Usage statistics
   - Feature availability

## Files Structure

### New Files Created

```
jarvis/
├── database.py              # Database management
├── account_manager.py       # Account and subscription logic
├── auth_ui.py              # Authentication UI windows
├── jarvis_data.db          # Local database (auto-created)
└── main.py                 # Updated with new features
```

### Database Schema

**Users Table**
- id, username, password, email
- subscription_tier, created_at, last_login
- queries_used, max_queries

**Chat History Table**
- id, user_id, query, response
- timestamp, session_id

**Subscriptions Table**
- id, user_id, tier, max_queries
- voice_enabled, ad_free, priority_support
- start_date, end_date, auto_renew

**Sessions Table**
- id, user_id, session_id
- created_at, last_active, is_active

## Features in Detail

### Query Limits
- **Free Tier**: 100 queries/month
- **Pro Tier**: 1000 queries/month
- **Premium Tier**: 10,000 queries/month
- When limit reached, upgrade to continue

### Voice Input
- Available on all tiers
- Pro and Premium tiers get priority processing

### Chat Persistence
- Conversations saved automatically
- View full history anytime
- Search through past conversations
- Export history (coming soon)

### Priority Support
- Premium tier users get 24/7 support
- Faster response times
- Dedicated support channel

## Security Features

- Passwords are hashed using SHA-256
- Local SQLite database (secure storage)
- Session management
- User isolation (only view own data)

## Troubleshooting

### Database Issues
If you encounter database errors:
1. Delete `jarvis_data.db`
2. Restart the application
3. Database will be recreated

### Forgot Password
- Currently no password recovery
- Create a new account or use guest mode
- Future versions will include password reset

### Query Limit Reached
- Upgrade to Pro or Premium tier
- Free tier resets monthly
- Check "Account Info" for usage

## Future Enhancements

- [ ] Password reset functionality
- [ ] Payment integration
- [ ] Cloud sync across devices
- [ ] Chat search and filtering
- [ ] Export conversations as PDF
- [ ] Multi-device support
- [ ] Advanced analytics
- [ ] Custom themes for pro users

## API Usage

Each query to Jarvis AI costs from your subscription quota. The AI models used are:
- OpenRouter models (GPT-3.5, Claude, Llama, etc.)
- Free tier limited to gpt-3.5-turbo
- Pro/Premium tiers access all models

## Support

For issues or feature requests:
1. Check "Account Info" for subscription details
2. Contact support through menu
3. Check troubleshooting section

---

**Version**: 2.0+  
**Last Updated**: January 2026  
**Status**: Active Development
