import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_data.db")

class Database:
    """Database management for Jarvis"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                subscription_tier TEXT DEFAULT 'free',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                queries_used INTEGER DEFAULT 0,
                max_queries INTEGER DEFAULT 100,
                last_ip TEXT,
                device_memory BOOLEAN DEFAULT 0
            )
        ''')
        
        # Add new columns if they don't exist
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN last_ip TEXT')
        except:
            pass
        
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN device_memory BOOLEAN DEFAULT 0')
        except:
            pass
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                session_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE NOT NULL,
                tier TEXT DEFAULT 'free',
                max_queries INTEGER DEFAULT 100,
                max_concurrent_sessions INTEGER DEFAULT 1,
                voice_enabled BOOLEAN DEFAULT 1,
                ad_free BOOLEAN DEFAULT 0,
                priority_support BOOLEAN DEFAULT 0,
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                auto_renew BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_id TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # User Management
    def create_user(self, username, password, email):
        """Create new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
            ''', (username, password, email))
            
            user_id = cursor.lastrowid
            
            # Create default free subscription
            cursor.execute('''
                INSERT INTO subscriptions (user_id, tier, max_queries)
                VALUES (?, ?, ?)
            ''', (user_id, 'free', 100))
            
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            return None
    
    def authenticate_user(self, username, password):
        """Authenticate user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username, subscription_tier FROM users
            WHERE username = ? AND password = ?
        ''', (username, password))
        
        result = cursor.fetchone()
        
        if result:
            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = ? WHERE id = ?
            ''', (datetime.now(), result[0]))
            conn.commit()
        
        conn.close()
        return result
    
    def get_user(self, user_id):
        """Get user details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    # Subscription Management
    def upgrade_subscription(self, user_id, tier):
        """Upgrade user subscription"""
        tier_config = {
            'free': {'max_queries': 100, 'voice': True, 'ad_free': False, 'support': False},
            'pro': {'max_queries': 1000, 'voice': True, 'ad_free': True, 'support': True},
            'premium': {'max_queries': 10000, 'voice': True, 'ad_free': True, 'support': True},
        }
        
        if tier not in tier_config:
            return False
        
        config = tier_config[tier]
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET subscription_tier = ? WHERE id = ?
        ''', (tier, user_id))
        
        cursor.execute('''
            UPDATE subscriptions
            SET tier = ?, max_queries = ?, ad_free = ?, priority_support = ?
            WHERE user_id = ?
        ''', (tier, config['max_queries'], config['ad_free'], config['support'], user_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_subscription(self, user_id):
        """Get user subscription details"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM subscriptions WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    def check_query_limit(self, user_id):
        """Check if user has queries remaining"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT queries_used, subscription_tier FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return False
        
        # Free tier check
        if result[1] == 'free' and result[0] >= 100:
            return False
        
        return True
    
    def increment_query_count(self, user_id):
        """Increment user query count"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET queries_used = queries_used + 1 WHERE id = ?
        ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    # Chat History Management
    def save_chat_message(self, user_id, query, response, session_id=None):
        """Save chat message to history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_history (user_id, query, response, session_id)
            VALUES (?, ?, ?, ?)
        ''', (user_id, query, response, session_id))
        
        conn.commit()
        conn.close()
    
    def get_chat_history(self, user_id, limit=50, session_id=None):
        """Get user chat history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute('''
                SELECT query, response, timestamp FROM chat_history
                WHERE user_id = ? AND session_id = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (user_id, session_id, limit))
        else:
            cursor.execute('''
                SELECT query, response, timestamp FROM chat_history
                WHERE user_id = ?
                ORDER BY timestamp DESC LIMIT ?
            ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return list(reversed(results))
    
    def get_chat_statistics(self, user_id):
        """Get chat statistics for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total chats
        cursor.execute('''
            SELECT COUNT(*) FROM chat_history WHERE user_id = ?
        ''', (user_id,))
        total_chats = cursor.fetchone()[0]
        
        # Today's chats
        cursor.execute('''
            SELECT COUNT(*) FROM chat_history
            WHERE user_id = ? AND DATE(timestamp) = DATE('now')
        ''', (user_id,))
        today_chats = cursor.fetchone()[0]
        
        conn.close()
        return {'total': total_chats, 'today': today_chats}
    
    def clear_chat_history(self, user_id, session_id=None):
        """Clear chat history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute('''
                DELETE FROM chat_history WHERE user_id = ? AND session_id = ?
            ''', (user_id, session_id))
        else:
            cursor.execute('''
                DELETE FROM chat_history WHERE user_id = ?
            ''', (user_id,))
        
        conn.commit()
        conn.close()
    
    # Session Management
    def create_session(self, user_id, session_id):
        """Create new session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO sessions (user_id, session_id)
            VALUES (?, ?)
        ''', (user_id, session_id))
        
        conn.commit()
        conn.close()
    
    def update_session_activity(self, session_id):
        """Update session last activity time"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE sessions SET last_active = ? WHERE session_id = ?
        ''', (datetime.now(), session_id))
        
        conn.commit()
        conn.close()
    
    # IP-based Device Memory
    def update_user_ip(self, user_id, ip_address):
        """Update user's last login IP"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_ip = ?, device_memory = 1 WHERE id = ?
        ''', (ip_address, user_id))
        
        conn.commit()
        conn.close()
    
    def get_user_last_ip(self, user_id):
        """Get user's last login IP"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT last_ip FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def is_device_memory_enabled(self, user_id):
        """Check if user has device memory enabled"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT device_memory FROM users WHERE id = ?
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else False
    
    def get_user_by_ip(self, ip_address):
        """Get user from their stored IP"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, username FROM users WHERE last_ip = ? AND device_memory = 1
        ''', (ip_address,))
        
        result = cursor.fetchone()
        conn.close()
        return result    
    def get_recent_chats(self, user_id, limit=10):
        """Get recent chats for user sidebar"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, query, response, timestamp FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def save_chat_history(self, user_id, title, content, session_id):
        """Save a chat session to history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO chat_history (user_id, query, response, session_id)
            VALUES (?, ?, ?, ?)
        ''', (user_id, title, content, session_id))
        
        conn.commit()
        conn.close()