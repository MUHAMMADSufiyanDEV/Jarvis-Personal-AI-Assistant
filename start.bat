@echo off
REM Quick Start Script for Jarvis Web App (Windows)

echo.
echo 🚀 Starting Jarvis Web App...
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements-web.txt
pip install gunicorn

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    (
        echo OPENROUTER_API_KEY=your_key_here
        echo SECRET_KEY=your_secret_key_here
    ) > .env
    echo ⚠️  Please update .env with your OPENROUTER_API_KEY
)

REM Run the app
echo ✅ Starting Flask app on http://localhost:5000
echo.
python app.py

REM Alternative: use Gunicorn for production
REM gunicorn app:app --workers 4 --worker-class sync --bind 0.0.0.0:5000

pause
