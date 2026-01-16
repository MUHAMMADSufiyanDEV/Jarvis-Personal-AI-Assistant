#!/bin/bash
# Quick Start Script for Jarvis Web App

echo "🚀 Starting Jarvis Web App..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements-web.txt
pip install gunicorn

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    echo "OPENROUTER_API_KEY=your_key_here" > .env
    echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" >> .env
    echo "⚠️  Please update .env with your OPENROUTER_API_KEY"
fi

# Run the app
echo "✅ Starting Flask app on http://localhost:5000"
python app.py

# Alternative: use Gunicorn for production
# gunicorn app:app --workers 4 --worker-class sync --bind 0.0.0.0:5000
