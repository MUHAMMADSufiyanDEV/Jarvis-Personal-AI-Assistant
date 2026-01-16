import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from account_manager import AccountManager, SubscriptionManager
from database import Database
import datetime
import uuid

class AuthenticationWindow:
    """Login and Registration UI"""
    
    def __init__(self, parent_callback):
        self.parent_callback = parent_callback
        self.account_manager = AccountManager()
        self.window = tk.Tk()
        self.window.title("🤖 Jarvis - Login/Register")
        self.window.geometry("500x600")
        self.window.configure(bg="#1a1a1a")
        self.window.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup authentication UI"""
        # Title
        title_label = tk.Label(
            self.window,
            text="🤖 JARVIS",
            font=("Helvetica", 28, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"
        )
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.window,
            text="AI Assistant",
            font=("Helvetica", 12),
            bg="#1a1a1a",
            fg="#888888"
        )
        subtitle_label.pack()
        
        # Check for device memory (IP-based auto-login)
        self.check_device_memory()
        
        # Frame for login/register
        self.main_frame = tk.Frame(self.window, bg="#1a1a1a")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show login screen initially
        self.show_login()
    
    def check_device_memory(self):
        """Check if device is recognized by IP"""
        current_ip = self.account_manager.check_ip_device_memory()
        user_data = self.account_manager.get_user_for_ip(current_ip)
        
        if user_data:
            # Auto-login
            user_id, username = user_data
            self.account_manager.current_user = {
                'id': user_id,
                'username': username,
                'tier': 'free'  # Will be updated from DB
            }
            self.account_manager.current_session = str(uuid.uuid4())
            self.account_manager.db.create_session(user_id, self.account_manager.current_session)
            self.account_manager.enable_device_memory(user_id)
            
            # Update last login
            user = self.account_manager.db.get_user(user_id)
            if user:
                self.account_manager.current_user['tier'] = user[4]
                self.account_manager.db.authenticate_user(user[1], user[2])  # Update last login
            
            # Close and callback
            self.window.after(500, lambda: self.auto_login_callback())
    
    def clear_frame(self):
        """Clear main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_login(self):
        """Show login screen"""
        self.clear_frame()
        
        # Username
        tk.Label(self.main_frame, text="Username:", font=("Helvetica", 10, "bold"), bg="#1a1a1a", fg="#ffffff").pack(anchor=tk.W, pady=(10, 0))
        username_entry = tk.Entry(self.main_frame, font=("Helvetica", 10), bg="#2a2a2a", fg="#ffffff", relief=tk.FLAT, insertbackground="#00ff00")
        username_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Password
        tk.Label(self.main_frame, text="Password:", font=("Helvetica", 10, "bold"), bg="#1a1a1a", fg="#ffffff").pack(anchor=tk.W, pady=(10, 0))
        password_entry = tk.Entry(self.main_frame, font=("Helvetica", 10), bg="#2a2a2a", fg="#ffffff", relief=tk.FLAT, insertbackground="#00ff00", show="●")
        password_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Login button
        login_btn = tk.Button(
            self.main_frame,
            text="Login",
            font=("Helvetica", 11, "bold"),
            bg="#00ff00",
            fg="#000000",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.handle_login(username_entry.get(), password_entry.get())
        )
        login_btn.pack(fill=tk.X, pady=10)
        
        # Or label
        or_label = tk.Label(self.main_frame, text="─ OR ─", font=("Helvetica", 10), bg="#1a1a1a", fg="#666666")
        or_label.pack(pady=15)
        
        # Register button
        register_btn = tk.Button(
            self.main_frame,
            text="Create New Account",
            font=("Helvetica", 11, "bold"),
            bg="#4a4a4a",
            fg="#ffffff",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_register
        )
        register_btn.pack(fill=tk.X, pady=10)
        
        # Guest login
        guest_btn = tk.Button(
            self.main_frame,
            text="Continue as Guest",
            font=("Helvetica", 10),
            bg="#2a2a2a",
            fg="#888888",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.handle_guest_login
        )
        guest_btn.pack(fill=tk.X, pady=10)
    
    def show_register(self):
        """Show registration screen"""
        self.clear_frame()
        
        # Username
        tk.Label(self.main_frame, text="Username:", font=("Helvetica", 10, "bold"), bg="#1a1a1a", fg="#ffffff").pack(anchor=tk.W, pady=(10, 0))
        username_entry = tk.Entry(self.main_frame, font=("Helvetica", 10), bg="#2a2a2a", fg="#ffffff", relief=tk.FLAT, insertbackground="#00ff00")
        username_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        tk.Label(self.main_frame, text="Email:", font=("Helvetica", 10, "bold"), bg="#1a1a1a", fg="#ffffff").pack(anchor=tk.W, pady=(10, 0))
        email_entry = tk.Entry(self.main_frame, font=("Helvetica", 10), bg="#2a2a2a", fg="#ffffff", relief=tk.FLAT, insertbackground="#00ff00")
        email_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Password
        tk.Label(self.main_frame, text="Password (min 6 chars):", font=("Helvetica", 10, "bold"), bg="#1a1a1a", fg="#ffffff").pack(anchor=tk.W, pady=(10, 0))
        password_entry = tk.Entry(self.main_frame, font=("Helvetica", 10), bg="#2a2a2a", fg="#ffffff", relief=tk.FLAT, insertbackground="#00ff00", show="●")
        password_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Confirm Password
        tk.Label(self.main_frame, text="Confirm Password:", font=("Helvetica", 10, "bold"), bg="#1a1a1a", fg="#ffffff").pack(anchor=tk.W, pady=(10, 0))
        confirm_entry = tk.Entry(self.main_frame, font=("Helvetica", 10), bg="#2a2a2a", fg="#ffffff", relief=tk.FLAT, insertbackground="#00ff00", show="●")
        confirm_entry.pack(fill=tk.X, pady=(0, 20))
        
        # Register button
        def handle_register():
            if password_entry.get() != confirm_entry.get():
                messagebox.showerror("Error", "Passwords do not match!")
                return
            
            success, message = self.account_manager.register_user(
                username_entry.get(),
                password_entry.get(),
                email_entry.get()
            )
            
            if success:
                messagebox.showinfo("Success", message)
                self.show_login()
            else:
                messagebox.showerror("Registration Failed", message)
        
        register_btn = tk.Button(
            self.main_frame,
            text="Register",
            font=("Helvetica", 11, "bold"),
            bg="#00ff00",
            fg="#000000",
            relief=tk.FLAT,
            cursor="hand2",
            command=handle_register
        )
        register_btn.pack(fill=tk.X, pady=10)
        
        # Back button
        back_btn = tk.Button(
            self.main_frame,
            text="Back to Login",
            font=("Helvetica", 10),
            bg="#2a2a2a",
            fg="#888888",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.show_login
        )
        back_btn.pack(fill=tk.X, pady=10)
    
    def handle_login(self, username, password):
        """Handle login"""
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter username and password")
            return
        
        success, message = self.account_manager.login_user(username, password)
        
        if success:
            messagebox.showinfo("Success", message)
            # Enable device memory for this device
            self.account_manager.enable_device_memory(self.account_manager.current_user['id'])
            self.window.destroy()
            self.parent_callback(self.account_manager)
        else:
            messagebox.showerror("Login Failed", message)
    
    def handle_guest_login(self):
        """Handle guest login"""
        self.window.destroy()
        self.parent_callback(None)
    
    def auto_login_callback(self):
        """Callback for auto-login via device memory"""
        self.window.destroy()
        self.parent_callback(self.account_manager)
    
    def run(self):
        """Run authentication window"""
        self.window.mainloop()


class SubscriptionWindow:
    """Subscription management window"""
    
    def __init__(self, parent, account_manager):
        self.parent = parent
        self.account_manager = account_manager
        self.db = Database()
        self.subscription_manager = SubscriptionManager(self.db)
        
        self.window = tk.Toplevel(parent)
        self.window.title("💎 Subscription Plans")
        self.window.geometry("900x500")
        self.window.configure(bg="#1a1a1a")
        self.window.resizable(False, False)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup subscription UI"""
        # Title
        title_label = tk.Label(
            self.window,
            text="💎 Choose Your Plan",
            font=("Helvetica", 18, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"
        )
        title_label.pack(pady=20)
        
        # Main frame for cards
        cards_frame = tk.Frame(self.window, bg="#1a1a1a")
        cards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Create subscription cards
        for tier_key, tier_data in self.subscription_manager.get_all_tiers().items():
            self.create_card(cards_frame, tier_key, tier_data)
    
    def create_card(self, parent, tier_key, tier_data):
        """Create subscription card"""
        card_frame = tk.Frame(parent, bg="#2a2a2a", highlightbackground="#00ff00", highlightthickness=2)
        card_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tier name
        name_label = tk.Label(
            card_frame,
            text=tier_data['name'],
            font=("Helvetica", 14, "bold"),
            bg="#2a2a2a",
            fg="#00ff00"
        )
        name_label.pack(pady=10)
        
        # Price
        price_label = tk.Label(
            card_frame,
            text=tier_data['price'],
            font=("Helvetica", 12, "bold"),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        price_label.pack(pady=5)
        
        # Features
        features_text = "\n".join(tier_data['features'])
        features_label = tk.Label(
            card_frame,
            text=features_text,
            font=("Helvetica", 9),
            bg="#2a2a2a",
            fg="#cccccc",
            justify=tk.LEFT
        )
        features_label.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Subscribe button
        btn = tk.Button(
            card_frame,
            text="Upgrade" if tier_key != 'free' else "Current",
            font=("Helvetica", 10, "bold"),
            bg="#00ff00" if tier_key != 'free' else "#666666",
            fg="#000000" if tier_key != 'free' else "#cccccc",
            relief=tk.FLAT,
            cursor="hand2",
            command=lambda: self.upgrade_plan(tier_key) if tier_key != 'free' else None
        )
        btn.pack(pady=10, padx=10, fill=tk.X)
    
    def upgrade_plan(self, tier):
        """Upgrade subscription plan"""
        if self.account_manager:
            # Show payment popup
            PaymentWindow(self.window, tier, self.account_manager, self.db)
        else:
            messagebox.showinfo("Guest", "Please login to upgrade subscription")


class PaymentWindow:
    """Payment popup window"""
    
    def __init__(self, parent, tier, account_manager, db):
        self.parent = parent
        self.tier = tier
        self.account_manager = account_manager
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("💳 Payment Options")
        self.window.geometry("400x300")
        self.window.configure(bg="#1a1a1a")
        self.window.resizable(False, False)
        self.window.grab_set()  # Make it modal
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup payment UI"""
        # Title
        title_label = tk.Label(
            self.window,
            text=f"💳 Upgrade to {self.tier.upper()}",
            font=("Helvetica", 14, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"
        )
        title_label.pack(pady=15)
        
        # Price
        prices = {'pro': '$9.99/month', 'premium': '$19.99/month'}
        price_label = tk.Label(
            self.window,
            text=f"Price: {prices.get(self.tier, 'Free')}",
            font=("Helvetica", 11),
            bg="#1a1a1a",
            fg="#ffffff"
        )
        price_label.pack(pady=5)
        
        # Separator
        separator = tk.Label(
            self.window,
            text="─" * 40,
            font=("Helvetica", 9),
            bg="#1a1a1a",
            fg="#444444"
        )
        separator.pack(pady=10)
        
        # Payment methods
        methods_frame = tk.Frame(self.window, bg="#1a1a1a")
        methods_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Bank Transfer
        bank_btn = tk.Button(
            methods_frame,
            text="🏦 Bank Transfer",
            font=("Helvetica", 10, "bold"),
            bg="#64b5f6",
            fg="#000000",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=lambda: self.process_payment("Bank Transfer")
        )
        bank_btn.pack(fill=tk.X, pady=5)
        
        # PayPal
        paypal_btn = tk.Button(
            methods_frame,
            text="🅿️ PayPal",
            font=("Helvetica", 10, "bold"),
            bg="#0070ba",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=lambda: self.process_payment("PayPal")
        )
        paypal_btn.pack(fill=tk.X, pady=5)
        
        # Payoneer
        payoneer_btn = tk.Button(
            methods_frame,
            text="💰 Payoneer",
            font=("Helvetica", 10, "bold"),
            bg="#118800",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=lambda: self.process_payment("Payoneer")
        )
        payoneer_btn.pack(fill=tk.X, pady=5)
        
        # Cancel button
        cancel_btn = tk.Button(
            methods_frame,
            text="❌ Cancel",
            font=("Helvetica", 10),
            bg="#ff6b6b",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.window.destroy
        )
        cancel_btn.pack(fill=tk.X, pady=5)
    
    def process_payment(self, method):
        """Process payment"""
        messagebox.showinfo(
            "Payment",
            f"Payment method: {method}\n\n"
            f"Tier: {self.tier.upper()}\n\n"
            f"You will be redirected to {method}.\n"
            f"After successful payment, your subscription will be activated.\n\n"
            f"[Demo: In production, this would redirect to payment gateway]"
        )
        
        # Upgrade subscription
        success, message = self.account_manager.upgrade_tier(self.tier)
        
        if success:
            # Enable device memory
            self.account_manager.enable_device_memory(self.account_manager.current_user['id'])
            messagebox.showinfo("Success", f"✅ {message}\n\nDevice memory enabled!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", message)


class ChatHistoryWindow:
    """Chat history browser window"""
    
    def __init__(self, parent, user_id, db):
        self.parent = parent
        self.user_id = user_id
        self.db = db
        
        self.window = tk.Toplevel(parent)
        self.window.title("📜 Chat History")
        self.window.geometry("700x500")
        self.window.configure(bg="#1a1a1a")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup chat history UI"""
        # Title
        title_label = tk.Label(
            self.window,
            text="📜 Chat History",
            font=("Helvetica", 14, "bold"),
            bg="#1a1a1a",
            fg="#00ff00"
        )
        title_label.pack(pady=10)
        
        # Statistics
        stats = self.db.get_chat_statistics(self.user_id)
        stats_label = tk.Label(
            self.window,
            text=f"Total: {stats['total']} chats | Today: {stats['today']} chats",
            font=("Helvetica", 9),
            bg="#1a1a1a",
            fg="#888888"
        )
        stats_label.pack()
        
        # Chat display
        display_frame = tk.Frame(self.window, bg="#1a1a1a")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(display_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        chat_display = scrolledtext.ScrolledText(
            display_frame,
            bg="#2a2a2a",
            fg="#ffffff",
            font=("Courier", 9),
            yscrollcommand=scrollbar.set
        )
        chat_display.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=chat_display.yview)
        
        # Get and display history
        history = self.db.get_chat_history(self.user_id, limit=100)
        for query, response, timestamp in history:
            chat_display.insert(tk.END, f"[{timestamp}]\n")
            chat_display.insert(tk.END, f"You: {query}\n", "user")
            chat_display.insert(tk.END, f"Jarvis: {response}\n\n", "jarvis")
        
        chat_display.config(state=tk.DISABLED)
        chat_display.tag_config("user", foreground="#00ff00")
        chat_display.tag_config("jarvis", foreground="#64b5f6")
