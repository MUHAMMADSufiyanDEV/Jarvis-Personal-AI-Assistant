import tkinter as tk
from tkinter import messagebox, ttk
import hashlib
import uuid
import socket
from database import Database

class AccountManager:
    """Manages user accounts and authentication"""
    
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.current_session = None
    
    @staticmethod
    def hash_password(password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, password, email):
        """Register new user"""
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        if "@" not in email:
            return False, "Invalid email format"
        
        hashed_password = self.hash_password(password)
        user_id = self.db.create_user(username, hashed_password, email)
        
        if user_id:
            return True, f"Account created successfully! Welcome {username}"
        else:
            return False, "Username or email already exists"
    
    def login_user(self, username, password):
        """Login user"""
        hashed_password = self.hash_password(password)
        result = self.db.authenticate_user(username, hashed_password)
        
        if result:
            self.current_user = {
                'id': result[0],
                'username': result[1],
                'tier': result[2]
            }
            self.current_session = str(uuid.uuid4())
            self.db.create_session(self.current_user['id'], self.current_session)
            return True, f"Welcome back, {username}!"
        else:
            return False, "Invalid username or password"
    
    def logout_user(self):
        """Logout user"""
        self.current_user = None
        self.current_session = None
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user is not None
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def get_current_session(self):
        """Get current session ID"""
        return self.current_session
    
    def upgrade_tier(self, tier):
        """Upgrade user subscription tier"""
        if not self.is_logged_in():
            return False, "Not logged in"
        
        success = self.db.upgrade_subscription(self.current_user['id'], tier)
        if success:
            self.current_user['tier'] = tier
            return True, f"Upgraded to {tier} tier!"
        return False, "Invalid tier"
    
    @staticmethod
    def get_device_ip():
        """Get device IP address"""
        try:
            # Get hostname
            hostname = socket.gethostname()
            # Get IP from hostname
            ip_address = socket.gethostbyname(hostname)
            return ip_address
        except:
            return "Unknown"
    
    def check_ip_device_memory(self):
        """Check if current device is recognized"""
        current_ip = self.get_device_ip()
        # Store for later use
        self.current_ip = current_ip
        return current_ip
    
    def enable_device_memory(self, user_id):
        """Enable device memory for current device"""
        current_ip = self.get_device_ip()
        self.db.update_user_ip(user_id, current_ip)
        self.current_ip = current_ip
    
    def get_user_for_ip(self, ip_address):
        """Get user info for given IP"""
        return self.db.get_user_by_ip(ip_address)


class SubscriptionManager:
    """Manages subscriptions and tiers"""
    
    TIERS = {
        'free': {
            'name': 'Free',
            'price': '$0/month',
            'queries': 100,
            'features': [
                '✓ 100 queries/month',
                '✓ Voice input',
                '✓ Chat history (7 days)',
                '✓ Basic support'
            ]
        },
        'pro': {
            'name': 'Pro',
            'price': '$9.99/month',
            'queries': 1000,
            'features': [
                '✓ 1000 queries/month',
                '✓ Voice input (priority)',
                '✓ Unlimited chat history',
                '✓ Priority support',
                '✓ Ad-free experience',
                '✓ Advanced features'
            ]
        },
        'premium': {
            'name': 'Premium',
            'price': '$19.99/month',
            'queries': 10000,
            'features': [
                '✓ 10,000 queries/month',
                '✓ Priority voice processing',
                '✓ Unlimited chat history',
                '✓ 24/7 Premium support',
                '✓ Ad-free experience',
                '✓ All advanced features',
                '✓ Custom settings',
                '✓ Early access to new features'
            ]
        }
    }
    
    def __init__(self, db):
        self.db = db
    
    def get_tier_info(self, tier):
        """Get subscription tier information"""
        return self.TIERS.get(tier)
    
    def get_all_tiers(self):
        """Get all available tiers"""
        return self.TIERS
    
    def get_user_tier_info(self, user_id):
        """Get user's current tier info"""
        user = self.db.get_user(user_id)
        if user:
            tier = user[4]  # subscription_tier
            return self.get_tier_info(tier)
        return None
    
    def get_user_queries_remaining(self, user_id):
        """Get remaining queries for user"""
        user = self.db.get_user(user_id)
        if user:
            queries_used = user[7]  # queries_used
            max_queries = user[8]  # max_queries
            return max_queries - queries_used
        return 0
    
    def get_subscription_details(self, user_id):
        """Get detailed subscription info"""
        subscription = self.db.get_subscription(user_id)
        if subscription:
            return {
                'tier': subscription[2],
                'max_queries': subscription[3],
                'voice_enabled': subscription[4],
                'ad_free': subscription[5],
                'priority_support': subscription[6],
                'start_date': subscription[7]
            }
        return None
