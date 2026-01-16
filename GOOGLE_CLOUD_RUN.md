# Deploy to Google Cloud Run (FREE)

## ⚡ Quick Deploy - 10 Minutes

### Prerequisites
- Google account (free)
- Code on GitHub ✅ (already done)
- gcloud CLI installed

---

## Step 1: Install gcloud CLI (3 min)

**Windows:**
```
1. Go to https://cloud.google.com/sdk/docs/install-sdk#windows
2. Download installer
3. Run installer
4. Open PowerShell and verify:
   gcloud --version
```

**Mac:**
```
brew install --cask google-cloud-sdk
gcloud --version
```

**Linux:**
```
curl https://sdk.cloud.google.com | bash
gcloud --version
```

---

## Step 2: Setup Google Cloud (2 min)

```powershell
# Login to Google
gcloud auth login

# Set your project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable build.googleapis.com
```

---

## Step 3: Create .gcloudignore (1 min)

Create file: `.gcloudignore` in your jarvis folder:

```
# Python files
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Other
.git/
.gitignore
README.md
*.md
Compressed/
Music/
Video/
New folder/
e36d71-*/
Programs/
Documents/
*.torrent
*.jfif
*.html
*.csv
*.txt
```

---

## Step 4: Deploy (2 min)

```powershell
# Navigate to jarvis folder
cd "c:\Users\REHMAN COMPUTER\Downloads\jarvis"

# Deploy to Cloud Run
gcloud run deploy jarvis-ai `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars="OPENROUTER_API_KEY=YOUR_API_KEY_HERE"
```

---

## Step 5: Get Your Live URL ✅

After deployment completes:
```
✓ Deploying... done.
Service [jarvis-ai] revision [jarvis-ai-001] has been deployed and is serving 100 percent of traffic.
Service URL: https://jarvis-ai-abc123.run.app
```

**Your app is LIVE!** 🌍

---

## Usage

**Share this URL with anyone:**
```
https://jarvis-ai-abc123.run.app
```

They can:
- Create account
- Chat with AI
- Export conversations
- All for free!

---

## Update App

Make changes → Push to GitHub → Redeploy:

```powershell
# Push to GitHub
git add .
git commit -m "Update message"
git push origin main

# Redeploy
gcloud run deploy jarvis-ai `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars="OPENROUTER_API_KEY=YOUR_API_KEY"
```

---

## Monitor & Logs

```powershell
# View logs
gcloud run logs read jarvis-ai --limit 50

# Check service status
gcloud run services describe jarvis-ai

# List all services
gcloud run services list
```

---

## 💰 FREE Tier Limits

✅ 2 million requests per month (FREE!)
✅ 360,000 GB-seconds of compute per month
✅ Automatic scaling
✅ Custom domain support (optional)

Most apps use way less than this!

---

## Troubleshooting

**Error: Permission denied**
```
gcloud auth login
```

**Error: Project not set**
```
gcloud config set project YOUR-PROJECT-ID
```

**API Key not working**
```
# Redeploy with correct key
gcloud run deploy jarvis-ai \
  --update-env-vars="OPENROUTER_API_KEY=your_new_key"
```

**App slow**
```
Cloud Run auto-scales. First request is slow, then it's fast!
```

---

## Success Checklist

- [ ] gcloud CLI installed
- [ ] Google account created
- [ ] GitHub code pushed
- [ ] .gcloudignore created
- [ ] OPENROUTER_API_KEY obtained
- [ ] Deploy command executed
- [ ] Live URL received
- [ ] Tested in browser
- [ ] Shared with friends

🎉 **Done!** Your AI is online!
