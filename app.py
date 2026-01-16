from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from functools import wraps
import json
import os
import uuid
import requests
from datetime import datetime
from database import Database
from account_manager import AccountManager, SubscriptionManager
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'jarvis-secret-key-change-in-production')
CORS(app)

# Initialize database and managers
db = Database()
subscription_manager = SubscriptionManager(db)

# OpenRouter API
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', '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')
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Instant responses knowledge base
INSTANT_RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! What can I do for you?",
    "how are you": "I'm doing great, thank you for asking!",
    "who are you": "I'm Jarvis, your personal AI assistant. I can answer questions, help with tasks, and much more!",
    "what's your name": "I'm Jarvis, your intelligent AI assistant!",
    "what can you do": "I can answer any question, help with tasks, provide information, and assist with various needs!",
    "help": "Ask me anything! I can answer questions, provide information, help with tasks, and more!",
}

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

def hash_password(password):
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.json
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not all([username, email, password]):
        return jsonify({'error': 'All fields required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    hashed_password = hash_password(password)
    user_id = db.create_user(username, hashed_password, email)
    
    if not user_id:
        return jsonify({'error': 'Username or email already exists'}), 400
    
    session['user_id'] = user_id
    session['username'] = username
    session['tier'] = 'free'
    
    return jsonify({'success': True, 'user_id': user_id})

@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    hashed_password = hash_password(password)
    result = db.authenticate_user(username, hashed_password)
    
    if not result:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    user_id, username, tier = result
    session['user_id'] = user_id
    session['username'] = username
    session['tier'] = tier
    session['session_id'] = str(uuid.uuid4())
    
    return jsonify({
        'success': True,
        'user_id': user_id,
        'username': username,
        'tier': tier
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'success': True})

@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    """Get current user info"""
    user = db.get_user(session['user_id'])
    if user:
        return jsonify({
            'id': user[0],
            'username': user[1],
            'email': user[3],
            'tier': user[4],
            'created_at': str(user[5])
        })
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """Process chat message"""
    data = request.json
    message = data.get('message', '').strip()
    
    if not message:
        return jsonify({'error': 'Empty message'}), 400
    
    user_id = session['user_id']
    
    # Check query limit
    if session['tier'] == 'free':
        if not db.check_query_limit(user_id):
            return jsonify({
                'error': 'Query limit reached',
                'message': '⚠️ You have reached your free tier limit (100/month). Please upgrade to continue!'
            }), 429
    
    # Get response
    response = get_smart_response(message)
    
    # Save to history
    session_id = session.get('session_id', str(uuid.uuid4()))
    db.save_chat_message(user_id, message, response, session_id)
    db.increment_query_count(user_id)
    
    return jsonify({
        'success': True,
        'message': message,
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/chat-history', methods=['GET'])
@login_required
def chat_history():
    """Get chat history"""
    user_id = session['user_id']
    limit = request.args.get('limit', 50, type=int)
    
    history = db.get_chat_history(user_id, limit)
    return jsonify({
        'history': [
            {'query': h[0], 'response': h[1], 'timestamp': str(h[2])}
            for h in history
        ]
    })

@app.route('/api/recent-chats', methods=['GET'])
@login_required
def recent_chats():
    """Get recent chats"""
    user_id = session['user_id']
    chats = db.get_recent_chats(user_id, limit=10)
    
    return jsonify({
        'chats': [
            {
                'id': c[0],
                'preview': c[1][:50] + '...' if len(c[1]) > 50 else c[1],
                'full_text': c[1],
                'timestamp': str(c[3])
            }
            for c in chats
        ]
    })

@app.route('/api/subscription', methods=['GET'])
@login_required
def get_subscription():
    """Get subscription info"""
    user_id = session['user_id']
    sub = db.get_subscription(user_id)
    user = db.get_user(user_id)
    
    if sub and user:
        return jsonify({
            'tier': user[4],
            'max_queries': sub[3],
            'queries_used': user[7],
            'voice_enabled': sub[5],
            'ad_free': sub[6],
            'priority_support': sub[7]
        })
    return jsonify({'error': 'Subscription not found'}), 404

@app.route('/api/upgrade', methods=['POST'])
@login_required
def upgrade_subscription():
    """Upgrade subscription"""
    data = request.json
    tier = data.get('tier', '').strip()
    
    if tier not in ['pro', 'premium']:
        return jsonify({'error': 'Invalid tier'}), 400
    
    user_id = session['user_id']
    success = db.upgrade_subscription(user_id, tier)
    
    if success:
        session['tier'] = tier
        return jsonify({'success': True, 'tier': tier})
    
    return jsonify({'error': 'Upgrade failed'}), 400

def get_smart_response(message):
    """Generate smart response"""
    message_lower = message.lower().strip()
    
    # Check instant responses
    for key, response in INSTANT_RESPONSES.items():
        if key in message_lower:
            return response
    
    # Pattern-based responses
    if any(word in message_lower for word in ["thank", "thanks"]):
        return "You're welcome! Happy to help."
    
    if any(word in message_lower for word in ["sorry", "apologize"]):
        return "No problem at all!"
    
    # Use OpenRouter API for general queries
    if OPENROUTER_API_KEY:
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": message}],
                "max_tokens": 500
            }
            
            response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
        except Exception as e:
            print(f"API Error: {e}")
    
    return f"I understand: '{message}'. Set API key for full AI capabilities!"

@app.route('/api/export', methods=['POST'])
@login_required
def export_chat():
    """Export chat"""
    user_id = session['user_id']
    format_type = request.json.get('format', 'txt')
    
    history = db.get_chat_history(user_id, limit=100)
    
    if format_type == 'json':
        content = json.dumps({'messages': history}, indent=2)
        filename = f"jarvis_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    else:  # txt or md
        lines = []
        for query, response, timestamp in history:
            lines.append(f"USER: {query}")
            lines.append(f"JARVIS: {response}")
            lines.append(f"Time: {timestamp}")
            lines.append("-" * 50)
        content = "\n".join(lines)
        filename = f"jarvis_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    return jsonify({
        'success': True,
        'filename': filename,
        'content': content
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500"""
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
