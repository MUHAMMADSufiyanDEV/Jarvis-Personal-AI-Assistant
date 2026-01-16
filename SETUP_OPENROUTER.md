# 🤖 Jarvis AI Assistant - OpenRouter Setup Guide

## Getting Started with AI Capabilities

Jarvis now has full AI integration with OpenRouter API. This allows it to answer ANY question using advanced AI models!

### Step 1: Get Your Free OpenRouter API Key

1. Visit: https://openrouter.ai
2. Click "Sign Up" (or Sign In if you have an account)
3. Complete the registration
4. Go to your dashboard and copy your API Key
5. You get $5 free credits monthly!

### Step 2: Set Up the API Key

#### Option A: Environment Variable (Recommended)
Run this command in PowerShell:
```powershell
$env:OPENROUTER_API_KEY="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"
python main.py
```

#### Option B: Permanent Environment Variable (Windows)
1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Click "New" (under User variables)
5. Variable name: `OPENROUTER_API_KEY`
6. Variable value: `your_api_key_here`
7. Click OK, then restart your terminal

#### Option C: Edit the script directly (Not recommended)
Open `main.py` and change line:
```python
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
```
To:
```python
OPENROUTER_API_KEY = "your_api_key_here"
```

### Step 3: Run Jarvis

```powershell
cd "c:\Users\REHMAN COMPUTER\Downloads\jarvis"
python main.py
```

You should see "✅ AI Enabled" in the header!

## Available Models

OpenRouter provides access to multiple free and paid models:
- **gpt-3.5-turbo** (Free tier)
- **Claude-3 Sonnet**
- **Llama 2**
- **Mistral**
- And many more!

Current config uses `gpt-3.5-turbo` which is free.

## Features

### What Jarvis Can Do:
✅ Answer any question  
✅ Explain concepts  
✅ Write code  
✅ Tell time & date  
✅ Search Google  
✅ Open websites  
✅ Voice input & text input  
✅ Beautiful UI  

## Example Queries

Try asking:
- "What is quantum computing?"
- "How do I learn Python?"
- "Explain photosynthesis"
- "Write a Python function to calculate factorial"
- "What's the capital of France?"
- "Tell me a joke"
- "How do I make pasta?"

## Troubleshooting

### "Set OPENROUTER_API_KEY for AI"
**Solution:** Your API key is not set. Follow Step 2 above.

### API Request Times Out
**Solution:** Check your internet connection or try a simpler query.

### "Unable to connect to AI service"
**Solution:** 
- Check internet connection
- Verify API key is correct
- Visit https://status.openrouter.ai to check service status

### Rate Limited
**Solution:** You've used your free tier quota. Upgrade your plan or wait for next month.

## Pricing

OpenRouter offers:
- **Free:** $5/month worth of credits
- **Paid models:** Variable pricing (usually $0.001-0.05 per query)
- No credit card required for free tier

## Security Note

⚠️ Never share your API key publicly or commit it to version control!

Always use environment variables or `.env` files for sensitive data.

---

Enjoy unlimited AI conversations with Jarvis! 🚀
