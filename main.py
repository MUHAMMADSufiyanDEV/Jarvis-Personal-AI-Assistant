import sounddevice as sd
import json
import pyttsx3
import datetime
import webbrowser
import os
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
from vosk import Model, KaldiRecognizer
import requests
import subprocess
import pyautogui
import pyperclip
import psutil
import time
import platform
import shutil
import uuid
from dotenv import load_dotenv  # Load environment variables from .env file

# Load environment variables from .env file
load_dotenv()

# Import new modules
from database import Database
from account_manager import AccountManager, SubscriptionManager
from auth_ui import AuthenticationWindow, SubscriptionWindow, ChatHistoryWindow

# Initialize text-to-speech engine with fallback
engine = None
try:
    # Try to use a different driver for better stability
    if platform.system() == 'Windows':
        engine = pyttsx3.init('sapi5')  # Windows speech API
    else:
        engine = pyttsx3.init()
    
    # Configure voice
    try:
        voices = engine.getProperty('voices')
        if len(voices) > 1:
            engine.setProperty('voice', voices[1].id)  # Try alternative voice
    except:
        pass
    
    engine.setProperty("rate", 160)  # Slightly slower for clarity
    engine.setProperty("volume", 1.0)  # Max volume
    print("✓ Voice engine initialized successfully")
except Exception as e:
    print(f"⚠ Voice engine initialization failed: {e}")
    engine = None
    print("Voice output disabled - continuing without voice")

# OpenRouter API Configuration
# Try to get from environment first, then use hardcoded as fallback
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY', "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")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Get a free API key from https://openrouter.ai
# To set custom key, run: set OPENROUTER_API_KEY=your_key_here (Windows) or export OPENROUTER_API_KEY=your_key_here (Mac/Linux)
print(f"✓ Using API Key: {OPENROUTER_API_KEY[:20]}..." if OPENROUTER_API_KEY else "✗ No API key configured!")

# Common Applications Dictionary
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
    "discord": "discord.exe",
    "spotify": "spotify.exe",
    "vlc": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe",
    "blender": "blender.exe",
    "vscode": "code.exe",
    "visual studio": "devenv.exe",
    "gimp": "gimp.exe",
    "photoshop": "photoshop.exe",
}

# Use absolute path for the model
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vosk-model-small-en-us-0.15")

# Check if model exists
if not os.path.exists(model_path):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", f"Model not found at {model_path}\nPlease download it first.")
    root.destroy()
    exit(1)

model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

# Device Control Functions
def open_application(app_name):
    """Open an application by name"""
    try:
        app_name_lower = app_name.lower().strip()
        
        # Check if app is in predefined list
        if app_name_lower in APP_PATHS:
            app_path = APP_PATHS[app_name_lower]
            subprocess.Popen(app_path)
            return f"Opening {app_name}..."
        
        # Try to open using Windows search
        try:
            subprocess.Popen(f"start {app_name_lower}", shell=True)
            return f"Opening {app_name}..."
        except:
            # Try searching in Program Files
            program_files = [
                "C:\\Program Files",
                "C:\\Program Files (x86)",
                os.path.expanduser("~\\AppData\\Local\\Programs")
            ]
            
            for root_dir in program_files:
                if os.path.exists(root_dir):
                    for root, dirs, files in os.walk(root_dir):
                        for file in files:
                            if app_name_lower in file.lower() and file.endswith('.exe'):
                                app_path = os.path.join(root, file)
                                subprocess.Popen(app_path)
                                return f"Opening {app_name}..."
            
            return f"Could not find application '{app_name}'. Try being more specific."
    except Exception as e:
        return f"Error opening application: {str(e)}"

def send_whatsapp_message(contact_name, message):
    """Send WhatsApp message using WhatsApp Web"""
    try:
        # Open WhatsApp Web
        webbrowser.open("https://web.whatsapp.com")
        time.sleep(5)  # Wait for page to load
        
        # Search for contact
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.typewrite(contact_name, interval=0.05)
        pyautogui.press('enter')
        time.sleep(2)
        
        # Click on chat and send message
        pyautogui.hotkey('tab')
        time.sleep(1)
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.hotkey('enter')
        
        return f"Message sent to {contact_name} on WhatsApp"
    except Exception as e:
        return f"Error sending WhatsApp message: {str(e)}"

def control_system(command):
    """Control system operations"""
    command_lower = command.lower().strip()
    
    try:
        if "volume up" in command_lower:
            pyautogui.press('volumeup')
            return "Volume increased"
        
        elif "volume down" in command_lower:
            pyautogui.press('volumedown')
            return "Volume decreased"
        
        elif "mute" in command_lower:
            pyautogui.press('volumemute')
            return "System muted"
        
        elif "shutdown" in command_lower or "turn off" in command_lower:
            os.system("shutdown /s /t 30")
            return "System will shut down in 30 seconds"
        
        elif "restart" in command_lower or "reboot" in command_lower:
            os.system("shutdown /r /t 30")
            return "System will restart in 30 seconds"
        
        elif "lock" in command_lower:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return "System locked"
        
        elif "sleep" in command_lower or "hibernation" in command_lower:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "System going to sleep"
        
        elif "brightness" in command_lower:
            if "up" in command_lower or "increase" in command_lower:
                os.system("powershell (Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)")
                return "Brightness increased"
            elif "down" in command_lower or "decrease" in command_lower:
                os.system("powershell (Get-WmiObject -Namespace root\\wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,20)")
                return "Brightness decreased"
        
        return "Unknown system command"
    
    except Exception as e:
        return f"Error controlling system: {str(e)}"

def get_running_processes():
    """Get list of running applications"""
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                processes.append(proc.info['name'])
            except:
                pass
        return processes[:10]  # Return first 10
    except Exception as e:
        return f"Error getting processes: {str(e)}"

def close_application(app_name):
    """Close an application"""
    try:
        os.system(f"taskkill /IM {app_name}.exe /F")
        return f"Closed {app_name}"
    except Exception as e:
        return f"Error closing application: {str(e)}"

class JarvisGUI:
    def __init__(self, root, account_manager=None):
        self.root = root
        self.root.title("Jarvis - AI Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0d0d0d")
        
        # Account and database
        self.account_manager = account_manager
        self.db = Database()
        self.subscription_manager = SubscriptionManager(self.db)
        self.current_user = account_manager.get_current_user() if account_manager else None
        self.current_session = account_manager.get_current_session() if account_manager else str(uuid.uuid4())
        
        # Variables
        self.is_listening = False
        self.conversation_history = []
        self.sidebar_open = True
        
        # Create UI elements
        self.create_widgets()
        
        # Initial greeting
        if self.current_user:
            greeting = f"Welcome back, {self.current_user['username']}! How can I help you today?"
        else:
            greeting = "Hello! I am Jarvis (Guest). Offline and ready. Type or speak your commands!"
        self.add_message("Jarvis", greeting)
        
        # Load recent chats
        self.load_recent_chats()
    
    def load_recent_chats(self):
        """Load and display recent chats in sidebar"""
        try:
            self.history_listbox.delete(0, tk.END)
            
            if self.current_user:
                # Get recent chats from database
                recent_chats = self.db.get_recent_chats(self.current_user['id'], limit=10)
                
                if recent_chats:
                    for chat in recent_chats:
                        # Extract first message as preview
                        preview = chat[2][:40] + "..." if len(chat[2]) > 40 else chat[2]
                        self.history_listbox.insert(tk.END, f"📝 {preview}")
                else:
                    self.history_listbox.insert(tk.END, "No recent chats")
            else:
                self.history_listbox.insert(tk.END, "Login to see chat history")
            
            # Bind click event to load chat
            self.history_listbox.bind("<Double-Button-1>", self.on_chat_select)
        except Exception as e:
            print(f"Error loading recent chats: {e}")
            self.history_listbox.insert(tk.END, "Error loading chats")
    
    def on_chat_select(self, event):
        """Load selected chat from history"""
        selection = self.history_listbox.curselection()
        if selection:
            messagebox.showinfo("Chat Selected", "Loading chat from history...")
    
    def add_chat_to_history(self):
        """Save current chat to history"""
        if self.current_user and self.conversation_history:
            try:
                # Get first message as title
                first_msg = next((msg['message'] for msg in self.conversation_history if msg['sender'] == 'You'), 'New Chat')
                title = first_msg[:50]
                
                # Save to database
                self.db.save_chat_history(
                    self.current_user['id'],
                    title,
                    json.dumps(self.conversation_history),
                    str(uuid.uuid4())
                )
                
                # Reload recent chats display
                self.load_recent_chats()
            except Exception as e:
                print(f"Error saving chat: {e}")
    
    def create_widgets(self):
        """Create modern UI matching the reference design"""
        main_container = tk.Frame(self.root, bg="#0d0d0d")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # ============ SIDEBAR ============
        self.sidebar = tk.Frame(main_container, bg="#1a1a1a", width=280)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # Brand header
        brand_frame = tk.Frame(self.sidebar, bg="#1a1a1a", height=70)
        brand_frame.pack(fill=tk.X)
        brand_frame.pack_propagate(False)
        
        brand_label = tk.Label(
            brand_frame,
            text="🤖 JARVIS",
            font=("Helvetica", 16, "bold"),
            bg="#1a1a1a",
            fg="#10a37f"
        )
        brand_label.pack(pady=15)
        
        # Tabs/sections
        tabs_frame = tk.Frame(self.sidebar, bg="#1a1a1a")
        tabs_frame.pack(fill=tk.X, padx=12, pady=(10, 0))
        
        explorer_btn = tk.Button(
            tabs_frame,
            text="Explorer",
            font=("Helvetica", 10),
            bg="#333333",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.show_explorer
        )
        explorer_btn.pack(side=tk.LEFT, padx=5)
        
        pin_btn = tk.Button(
            tabs_frame,
            text="📌 Pin",
            font=("Helvetica", 10),
            bg="#1a1a1a",
            fg="#888888",
            relief=tk.FLAT,
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.show_pinned_chats
        )
        pin_btn.pack(side=tk.LEFT, padx=5)
        
        # New chat button
        new_chat_btn = tk.Button(
            self.sidebar,
            text="✨ New Chat",
            font=("Helvetica", 11, "bold"),
            bg="#10a37f",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=self.clear_chat
        )
        new_chat_btn.pack(fill=tk.X, padx=12, pady=15)
        
        # Chat history
        history_label = tk.Label(
            self.sidebar,
            text="Recent Chats",
            font=("Helvetica", 10, "bold"),
            bg="#1a1a1a",
            fg="#888888"
        )
        history_label.pack(anchor=tk.W, padx=15, pady=(20, 10))
        
        self.history_listbox = tk.Listbox(
            self.sidebar,
            bg="#1a1a1a",
            fg="#ececec",
            font=("Helvetica", 9),
            relief=tk.FLAT,
            borderwidth=0,
            height=15
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=12, pady=10)
        
        # Sidebar footer
        footer_frame = tk.Frame(self.sidebar, bg="#1a1a1a")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=12, pady=15)
        
        if self.current_user:
            user_label = tk.Label(
                footer_frame,
                text=f"👤 {self.current_user['username']}",
                font=("Helvetica", 9),
                bg="#1a1a1a",
                fg="#ececec"
            )
            user_label.pack(anchor=tk.W, pady=(0, 5))
            
            tier_label = tk.Label(
                footer_frame,
                text=f"🎯 {self.current_user['tier'].upper()}",
                font=("Helvetica", 8),
                bg="#1a1a1a",
                fg="#10a37f"
            )
            tier_label.pack(anchor=tk.W)
        
        # ============ MAIN CONTENT ============
        content_container = tk.Frame(main_container, bg="#0d0d0d")
        content_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Header with tools
        header = tk.Frame(content_container, bg="#0d0d0d", height=60)
        header.pack(fill=tk.X, padx=20, pady=15)
        header.pack_propagate(False)
        
        title_label = tk.Label(
            header,
            text="Chat with Jarvis",
            font=("Helvetica", 18, "bold"),
            bg="#0d0d0d",
            fg="#ffffff"
        )
        title_label.pack(side=tk.LEFT)
        
        # Right side header buttons
        header_buttons = tk.Frame(header, bg="#0d0d0d")
        header_buttons.pack(side=tk.RIGHT)
        
        settings_btn = tk.Button(
            header_buttons,
            text="⚙️ Settings",
            font=("Helvetica", 9),
            bg="#2d2d2d",
            fg="#888888",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.show_settings
        )
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        training_btn = tk.Button(
            header_buttons,
            text="📚 Training",
            font=("Helvetica", 9),
            bg="#2d2d2d",
            fg="#888888",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.show_training
        )
        training_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(
            header_buttons,
            text="📤 Export",
            font=("Helvetica", 9),
            bg="#2d2d2d",
            fg="#888888",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.show_export
        )
        export_btn.pack(side=tk.LEFT, padx=5)
        
        # Chat area
        chat_frame = tk.Frame(content_container, bg="#0d0d0d")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Segoe UI", 10),
            bg="#0d0d0d",
            fg="#ececec",
            insertbackground="#10a37f",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Text tags
        self.chat_display.tag_configure("user_bubble", foreground="#ffffff", background="#1f4620", font=("Segoe UI", 10))
        self.chat_display.tag_configure("jarvis_bubble", foreground="#ffffff", background="#2d2d44", font=("Segoe UI", 10))
        self.chat_display.tag_configure("user_label", foreground="#10a37f", font=("Segoe UI", 9, "bold"))
        self.chat_display.tag_configure("jarvis_label", foreground="#888888", font=("Segoe UI", 8, "bold"))
        self.chat_display.tag_configure("prompt_header", foreground="#e0e0e0", font=("Segoe UI", 11, "bold"))
        self.chat_display.tag_configure("prompt_text", foreground="#a0a0a0", font=("Segoe UI", 9))
        self.chat_display.tag_configure("prompt_button", foreground="#10a37f", font=("Segoe UI", 10))
        
        # Input area - bottom
        input_container = tk.Frame(content_container, bg="#0d0d0d")
        input_container.pack(fill=tk.X, padx=20, pady=15)
        
        # Input frame with rounded appearance
        input_frame = tk.Frame(input_container, bg="#2d2d2d", height=50)
        input_frame.pack(fill=tk.X)
        input_frame.pack_propagate(False)
        
        # Text input
        self.input_field = tk.Entry(
            input_frame,
            font=("Segoe UI", 11),
            bg="#2d2d2d",
            fg="#ececec",
            insertbackground="#10a37f",
            relief=tk.FLAT,
            borderwidth=0
        )
        self.input_field.pack(fill=tk.BOTH, expand=True, padx=15, pady=12)
        self.input_field.bind("<Return>", lambda e: self.send_text_command())
        self.input_field.insert(0, "Ask Jarvis anything...")
        self.input_field.bind("<FocusIn>", lambda e: self._on_input_focus_in())
        self.input_field.bind("<FocusOut>", lambda e: self._on_input_focus_out())
        
        # Bottom action bar
        action_bar = tk.Frame(input_container, bg="#0d0d0d")
        action_bar.pack(fill=tk.X, pady=(10, 0))
        
        left_buttons = tk.Frame(action_bar, bg="#0d0d0d")
        left_buttons.pack(side=tk.LEFT)
        
        # Microphone button
        self.voice_btn = tk.Button(
            left_buttons,
            text="🎤",
            font=("Helvetica", 10),
            bg="#2d2d2d",
            fg="#00d4ff",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.voice_input
        )
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        # New chat button
        new_btn = tk.Button(
            left_buttons,
            text="➕",
            font=("Helvetica", 10),
            bg="#2d2d2d",
            fg="#888888",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.clear_chat
        )
        new_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = tk.Button(
            left_buttons,
            text="🗑️",
            font=("Helvetica", 10),
            bg="#2d2d2d",
            fg="#ff6b6b",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.clear_chat
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Right buttons
        right_buttons = tk.Frame(action_bar, bg="#0d0d0d")
        right_buttons.pack(side=tk.RIGHT)
        
        # Subscriptions button
        if self.current_user:
            subs_btn = tk.Button(
                right_buttons,
                text="💎 Subscriptions",
                font=("Helvetica", 9),
                bg="#2d2d2d",
                fg="#ffa500",
                relief=tk.FLAT,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda: SubscriptionWindow(self.root, self.account_manager) if self.account_manager else messagebox.showinfo("Info", "Please login to access subscriptions")
            )
            subs_btn.pack(side=tk.LEFT, padx=5)
        
        # History button
        if self.current_user:
            history_btn = tk.Button(
                right_buttons,
                text="📜 History",
                font=("Helvetica", 9),
                bg="#2d2d2d",
                fg="#64b5f6",
                relief=tk.FLAT,
                padx=10,
                pady=5,
                cursor="hand2",
                command=lambda: ChatHistoryWindow(self.root, self.current_user['id'], self.db)
            )
            history_btn.pack(side=tk.LEFT, padx=5)
        
        # Send button (prominent)
        self.send_btn = tk.Button(
            right_buttons,
            text="Send",
            font=("Helvetica", 10, "bold"),
            bg="#10a37f",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.send_text_command
        )
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        # Toggle voice output
        self.voice_output_state = True
        self.voice_output_btn = tk.Button(
            right_buttons,
            text="🔊",
            font=("Helvetica", 10),
            bg="#2d2d2d",
            fg="#ffa500",
            relief=tk.FLAT,
            padx=10,
            pady=5,
            cursor="hand2",
            command=self.toggle_voice_output
        )
        self.voice_output_btn.pack(side=tk.LEFT, padx=5)
        
        # Show initial prompt suggestions if no messages yet
        self.show_welcome_prompts()
    
    def show_explorer(self):
        """Show chat explorer"""
        explorer_window = tk.Toplevel(self.root)
        explorer_window.title("Chat Explorer")
        explorer_window.geometry("350x400")
        explorer_window.configure(bg="#1a1a1a")
        
        title = tk.Label(
            explorer_window,
            text="📂 Chat Explorer",
            font=("Helvetica", 14, "bold"),
            bg="#1a1a1a",
            fg="#10a37f"
        )
        title.pack(pady=15)
        
        info = tk.Label(
            explorer_window,
            text="Browse all your conversations\nand organized chats here",
            font=("Helvetica", 10),
            bg="#1a1a1a",
            fg="#888888",
            justify=tk.CENTER
        )
        info.pack(pady=20)
        
        # Placeholder chat items
        for i in range(5):
            item = tk.Label(
                explorer_window,
                text=f"📄 Chat #{i+1}",
                font=("Helvetica", 9),
                bg="#2d2d2d",
                fg="#ececec",
                relief=tk.RAISED,
                padx=10,
                pady=8
            )
            item.pack(fill=tk.X, padx=15, pady=5)
    
    def show_pinned_chats(self):
        """Show pinned chats"""
        pinned_window = tk.Toplevel(self.root)
        pinned_window.title("Pinned Chats")
        pinned_window.geometry("350x300")
        pinned_window.configure(bg="#1a1a1a")
        
        title = tk.Label(
            pinned_window,
            text="📌 Pinned Chats",
            font=("Helvetica", 14, "bold"),
            bg="#1a1a1a",
            fg="#ffa500"
        )
        title.pack(pady=15)
        
        info = tk.Label(
            pinned_window,
            text="Pin important conversations\nfor quick access",
            font=("Helvetica", 10),
            bg="#1a1a1a",
            fg="#888888",
            justify=tk.CENTER
        )
        info.pack(pady=20)
        
        empty = tk.Label(
            pinned_window,
            text="No pinned chats yet",
            font=("Helvetica", 10, "italic"),
            bg="#1a1a1a",
            fg="#666666"
        )
        empty.pack(pady=20)
    
    def show_settings(self):
        """Show settings panel"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x500")
        settings_window.configure(bg="#1a1a1a")
        
        title = tk.Label(
            settings_window,
            text="⚙️ Settings",
            font=("Helvetica", 16, "bold"),
            bg="#1a1a1a",
            fg="#10a37f"
        )
        title.pack(pady=20)
        
        # Voice settings
        voice_frame = tk.LabelFrame(
            settings_window,
            text="🔊 Voice Settings",
            font=("Helvetica", 11, "bold"),
            bg="#2d2d2d",
            fg="#ececec",
            relief=tk.FLAT
        )
        voice_frame.pack(fill=tk.X, padx=20, pady=10)
        
        voice_speed_label = tk.Label(
            voice_frame,
            text="Voice Speed:",
            font=("Helvetica", 10),
            bg="#2d2d2d",
            fg="#ececec"
        )
        voice_speed_label.pack(anchor=tk.W, padx=15, pady=(10, 5))
        
        self.voice_speed_var = tk.IntVar(value=170)
        voice_speed = tk.Scale(
            voice_frame,
            from_=100,
            to=300,
            orient=tk.HORIZONTAL,
            bg="#333333",
            fg="#10a37f",
            troughcolor="#2d2d2d",
            variable=self.voice_speed_var
        )
        voice_speed.set(170)
        voice_speed.pack(fill=tk.X, padx=15, pady=10)
        
        # Theme settings
        theme_frame = tk.LabelFrame(
            settings_window,
            text="🎨 Theme",
            font=("Helvetica", 11, "bold"),
            bg="#2d2d2d",
            fg="#ececec",
            relief=tk.FLAT
        )
        theme_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.theme_var = tk.StringVar(value="dark")
        for theme_name in ["Dark Mode", "Light Mode"]:
            radio = tk.Radiobutton(
                theme_frame,
                text=theme_name,
                variable=self.theme_var,
                value=theme_name.lower().replace(" ", "_"),
                font=("Helvetica", 10),
                bg="#2d2d2d",
                fg="#ececec",
                selectcolor="#10a37f"
            )
            radio.pack(anchor=tk.W, padx=15, pady=5)
        
        # Save button
        def save_settings():
            # Apply voice speed
            global engine
            if engine:
                engine.setProperty("rate", self.voice_speed_var.get())
            
            # Apply theme
            theme = self.theme_var.get()
            self.apply_theme(theme)
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            settings_window.destroy()
        
        save_btn = tk.Button(
            settings_window,
            text="💾 Save Settings",
            font=("Helvetica", 11, "bold"),
            bg="#10a37f",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=save_settings
        )
        save_btn.pack(pady=20)
    
    def show_training(self):
        """Show training/documentation"""
        training_window = tk.Toplevel(self.root)
        training_window.title("Training")
        training_window.geometry("450x400")
        training_window.configure(bg="#1a1a1a")
        
        title = tk.Label(
            training_window,
            text="📚 Training & Help",
            font=("Helvetica", 16, "bold"),
            bg="#1a1a1a",
            fg="#10a37f"
        )
        title.pack(pady=20)
        
        help_text = tk.Text(
            training_window,
            font=("Segoe UI", 10),
            bg="#2d2d2d",
            fg="#ececec",
            relief=tk.FLAT,
            height=15,
            width=50,
            wrap=tk.WORD
        )
        help_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        help_content = """🤖 JARVIS AI Assistant - Quick Guide

📝 Basic Commands:
• Type any question or command
• Use 🎤 to speak your command
• Press Enter or click Send

🎙️ Voice Features:
• 🎤 Click to record voice input
• 🔊 Toggle voice output
• Adjust speed in Settings

💬 Chat Management:
• ➕ New Chat - Start fresh conversation
• 📜 History - View past chats
• 💎 Subscriptions - Upgrade tier

⚙️ Customization:
• ⚙️ Settings - Configure preferences
• 🎨 Choose your theme
• Adjust voice speed

📤 Export:
• Save chats as files
• Share conversations
• Backup your data

🔐 Account:
• 👤 Manage your profile
• View subscription status
• Track usage statistics
"""
        help_text.insert(1.0, help_content)
        help_text.config(state=tk.DISABLED)
    
    def show_export(self):
        """Show export options"""
        export_window = tk.Toplevel(self.root)
        export_window.title("Export")
        export_window.geometry("400x300")
        export_window.configure(bg="#1a1a1a")
        
        title = tk.Label(
            export_window,
            text="📤 Export Chat",
            font=("Helvetica", 16, "bold"),
            bg="#1a1a1a",
            fg="#10a37f"
        )
        title.pack(pady=20)
        
        # Export format options
        format_frame = tk.LabelFrame(
            export_window,
            text="Select Format",
            font=("Helvetica", 11, "bold"),
            bg="#2d2d2d",
            fg="#ececec",
            relief=tk.FLAT
        )
        format_frame.pack(fill=tk.X, padx=20, pady=10)
        
        format_var = tk.StringVar(value="txt")
        for fmt, ext in [("Text (.txt)", "txt"), ("JSON (.json)", "json"), ("Markdown (.md)", "md")]:
            radio = tk.Radiobutton(
                format_frame,
                text=fmt,
                variable=format_var,
                value=ext,
                font=("Helvetica", 10),
                bg="#2d2d2d",
                fg="#ececec",
                selectcolor="#10a37f"
            )
            radio.pack(anchor=tk.W, padx=15, pady=5)
        
        # Export button
        def export_chat():
            fmt = format_var.get()
            filename = self.export_conversation(fmt)
            if filename:
                messagebox.showinfo("Export Successful", f"Chat exported as {filename}!")
                export_window.destroy()
            else:
                messagebox.showerror("Export Failed", "Could not export chat")
        
        export_btn = tk.Button(
            export_window,
            text="📥 Export Now",
            font=("Helvetica", 11, "bold"),
            bg="#10a37f",
            fg="#ffffff",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=export_chat
        )
        export_btn.pack(pady=20)
    
    def show_menu(self):
        """Show menu with options"""
        menu_window = tk.Toplevel(self.root)
        menu_window.title("Menu")
        menu_window.geometry("250x200")
        menu_window.configure(bg="#1a1a1a")
        menu_window.resizable(False, False)
        
        # Subscription button
        sub_btn = tk.Button(
            menu_window,
            text="💎 Subscriptions",
            font=("Helvetica", 11, "bold"),
            bg="#00ff00",
            fg="#000000",
            relief=tk.FLAT,
            padx=15,
            pady=10,
            cursor="hand2",
            command=lambda: SubscriptionWindow(self.root, self.account_manager) if self.account_manager else messagebox.showinfo("Info", "Please login to access subscriptions")
        )
        sub_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Chat history button
        if self.current_user:
            history_btn = tk.Button(
                menu_window,
                text="📜 Chat History",
                font=("Helvetica", 11, "bold"),
                bg="#64b5f6",
                fg="#000000",
                relief=tk.FLAT,
                padx=15,
                pady=10,
                cursor="hand2",
                command=lambda: ChatHistoryWindow(self.root, self.current_user['id'], self.db)
            )
            history_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Account info button
        if self.current_user:
            account_btn = tk.Button(
                menu_window,
                text="👤 Account Info",
                font=("Helvetica", 11, "bold"),
                bg="#ffa500",
                fg="#000000",
                relief=tk.FLAT,
                padx=15,
                pady=10,
                cursor="hand2",
                command=self.show_account_info
            )
            account_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Logout button
        if self.current_user:
            logout_btn = tk.Button(
                menu_window,
                text="🚪 Logout",
                font=("Helvetica", 11, "bold"),
                bg="#ff6b6b",
                fg="#ffffff",
                relief=tk.FLAT,
                padx=15,
                pady=10,
                cursor="hand2",
                command=self.logout
            )
            logout_btn.pack(fill=tk.X, padx=10, pady=10)
    
    def show_account_info(self):
        """Show account information"""
        if not self.current_user:
            messagebox.showinfo("Info", "Not logged in")
            return
        
        user = self.db.get_user(self.current_user['id'])
        subscription = self.db.get_subscription(self.current_user['id'])
        stats = self.db.get_chat_statistics(self.current_user['id'])
        
        info_window = tk.Toplevel(self.root)
        info_window.title("Account Information")
        info_window.geometry("350x300")
        info_window.configure(bg="#1a1a1a")
        
        info_text = f"""
        👤 Username: {user[1]}
        📧 Email: {user[2]}
        💎 Subscription: {user[4].upper()}
        
        📊 Statistics:
        ├─ Total Chats: {stats['total']}
        ├─ Today's Chats: {stats['today']}
        ├─ Queries Used: {user[7]}/{user[8]}
        └─ Joined: {user[5]}
        
        ✨ Features:
        ├─ Voice Enabled: {'Yes' if subscription[4] else 'No'}
        ├─ Ad-Free: {'Yes' if subscription[5] else 'No'}
        └─ Priority Support: {'Yes' if subscription[6] else 'No'}
        """
        
        info_label = tk.Label(
            info_window,
            text=info_text,
            font=("Courier", 10),
            bg="#1a1a1a",
            fg="#00ff00",
            justify=tk.LEFT
        )
        info_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def logout(self):
        """Logout user"""
        if self.account_manager:
            self.account_manager.logout_user()
            messagebox.showinfo("Logout", "You have been logged out successfully")
            self.root.quit()
    
    def _on_input_focus_in(self):
        """Clear placeholder text on focus"""
        if self.input_field.get() == "Ask Jarvis anything...":
            self.input_field.delete(0, tk.END)
            self.input_field.config(fg="#ececec")
    
    def _on_input_focus_out(self):
        """Show placeholder text on focus out"""
        if self.input_field.get() == "":
            self.input_field.insert(0, "Ask Jarvis anything...")
            self.input_field.config(fg="#666666")
    
    def show_welcome_prompts(self):
        """Show welcome screen with suggested prompts"""
        if len(self.conversation_history) == 0:
            self.chat_display.config(state=tk.NORMAL)
            
            # Welcome header
            self.chat_display.insert(tk.END, "✨ Welcome to Jarvis AI\n", "prompt_header")
            self.chat_display.insert(tk.END, "\nHere are some sample questions to get started:\n\n", "prompt_text")
            
            # Sample prompts
            prompts = [
                "💡 What can you help me with?",
                "🔧 How do I open an application?",
                "📝 Can you summarize text for me?",
                "🎨 Help me create something creative"
            ]
            
            for prompt in prompts:
                self.chat_display.insert(tk.END, f"  • {prompt}\n", "prompt_button")
            
            self.chat_display.insert(tk.END, "\n")
            self.chat_display.config(state=tk.DISABLED)
    
    def add_message(self, sender, message):
        """Add message to chat display with styled bubbles"""
        self.chat_display.config(state=tk.NORMAL)
        
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "You":
            # User message - right-aligned with blue bubble
            self.chat_display.insert(tk.END, f"YOU • {timestamp}\n", "user_label")
            self.chat_display.insert(tk.END, f"  {message}\n", "user_bubble")
            self.chat_display.insert(tk.END, "\n")
        else:
            # Jarvis message - left-aligned with green bubble
            self.chat_display.insert(tk.END, f"JARVIS • {timestamp}\n", "jarvis_label")
            self.chat_display.insert(tk.END, f"  {message}\n", "jarvis_bubble")
            self.chat_display.insert(tk.END, "\n")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        self.conversation_history.append({"sender": sender, "message": message})
    
    def apply_theme(self, theme):
        """Apply theme to the application"""
        if theme == "dark_mode":
            bg_color = "#0d0d0d"
            fg_color = "#ececec"
            sidebar_bg = "#1a1a1a"
        else:  # light_mode
            bg_color = "#f5f5f5"
            fg_color = "#1a1a1a"
            sidebar_bg = "#e0e0e0"
        
        # Update main window and containers
        self.root.configure(bg=bg_color)
        self.chat_display.configure(bg=bg_color, fg=fg_color)
        messagebox.showinfo("Theme Applied", f"Switched to {theme.replace('_', ' ').title()}!")
    
    def export_conversation(self, format_type):
        """Export conversation to file"""
        import json
        from datetime import datetime
        
        if not self.conversation_history:
            messagebox.showwarning("No Chat", "No messages to export!")
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        try:
            if format_type == "txt":
                filename = f"jarvis_chat_{timestamp}.txt"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("=" * 60 + "\n")
                    f.write("JARVIS AI CHAT EXPORT\n")
                    f.write("=" * 60 + "\n\n")
                    for msg in self.conversation_history:
                        f.write(f"{msg['sender'].upper()}:\n")
                        f.write(f"{msg['message']}\n")
                        f.write("-" * 40 + "\n\n")
                
            elif format_type == "json":
                filename = f"jarvis_chat_{timestamp}.json"
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump({
                        "exported_at": datetime.now().isoformat(),
                        "messages": self.conversation_history
                    }, f, indent=2, ensure_ascii=False)
            
            elif format_type == "md":
                filename = f"jarvis_chat_{timestamp}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write("# JARVIS AI Chat Export\n\n")
                    f.write(f"*Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
                    for msg in self.conversation_history:
                        f.write(f"## {msg['sender']}\n")
                        f.write(f"{msg['message']}\n\n")
            
            print(f"✅ Chat exported to: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ Export failed: {str(e)}")
            return None
    
    def send_text_command(self):
        """Process text input"""
        command = self.input_field.get().strip()
        
        if not command:
            return
        
        # Check query limit for free tier
        if self.current_user and self.current_user['tier'] == 'free':
            if not self.db.check_query_limit(self.current_user['id']):
                self.add_message("System", "⚠️ You've reached your free tier query limit (100/month). Please upgrade to continue!")
                return
        
        self.add_message("You", command)
        self.input_field.delete(0, tk.END)
        
        # Process command in separate thread
        thread = threading.Thread(target=lambda: self.process_and_respond(command))
        thread.daemon = True
        thread.start()
    
    def voice_input(self):
        """Listen for voice input with better UI feedback"""
        if self.is_listening:
            messagebox.showwarning("Warning", "Already listening... please wait.")
            return
        
        try:
            self.add_message("System", "🎤 Listening... (5 seconds)")
            self.voice_btn.config(state=tk.DISABLED, text="⏳ Recording...")
            self.root.update()
            
            # Record in separate thread
            thread = threading.Thread(target=self.record_audio)
            thread.daemon = True
            thread.start()
        except Exception as e:
            print(f"Voice input error: {e}")
            messagebox.showerror("Error", f"Could not start voice input: {str(e)}")
            self.voice_btn.config(state=tk.NORMAL, text="🎤 Listen")
    
    def record_audio(self):
        """Record audio from microphone with improved error handling"""
        self.is_listening = True
        try:
            print("Recording audio...")
            try:
                # Try to record audio
                audio_data = sd.rec(int(5 * 16000), samplerate=16000, channels=1, dtype="int16")
                sd.wait()
                
                if audio_data is None or len(audio_data) == 0:
                    raise ValueError("No audio recorded")
                
                # Process audio
                if recognizer.AcceptWaveform(audio_data.tobytes()):
                    result = json.loads(recognizer.Result())
                    command = result.get("text", "").strip()
                    
                    if command:
                        print(f"✓ Recognized: {command}")
                        self.root.after(0, lambda: self.add_message("You", command))
                        self.root.after(0, lambda: self.process_and_respond(command))
                    else:
                        self.root.after(0, lambda: self.add_message("System", "Could not understand audio. Please try again."))
                else:
                    # Partial result
                    try:
                        partial = json.loads(recognizer.PartialResult())
                        partial_text = partial.get("partial", "").strip()
                        if partial_text:
                            print(f"Partial: {partial_text}")
                    except:
                        pass
                        
            except sd.PortAudioError:
                self.root.after(0, lambda: messagebox.showerror("Microphone Error", "No microphone detected. Please connect a microphone."))
            except Exception as e:
                print(f"Recording error: {str(e)}")
                self.root.after(0, lambda: messagebox.showerror("Error", f"Recording error: {str(e)}"))
        finally:
            self.is_listening = False
            self.root.after(0, lambda: self.voice_btn.config(state=tk.NORMAL, text="🎤 Listen"))
    
    def process_and_respond(self, command):
        """Process command and generate response"""
        response = self.get_smart_response(command)
        
        if response:
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            self.speak_response(response)
            
            # Save to chat history if user is logged in
            if self.current_user:
                self.db.save_chat_message(
                    self.current_user['id'],
                    command,
                    response,
                    self.current_session
                )
                # Increment query count
                self.db.increment_query_count(self.current_user['id'])
        
        # Check for action commands
        self.execute_action(command)
    
    def get_smart_response(self, command):
        """Generate intelligent responses using OpenRouter AI"""
        command_lower = command.lower().strip()
        
        # Knowledge base for instant responses (no API needed)
        instant_responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I do for you?",
            "how are you": "I'm doing great, thank you for asking!",
            "who are you": "I'm Jarvis, your personal AI assistant. I can answer questions, open apps, control your device, send messages, and much more!",
            "what's your name": "I'm Jarvis, your intelligent voice assistant!",
            "what can you do": "I can open/close applications, adjust volume and brightness, lock your system, search the web, send messages, answer any question, and much more!",
            "help": "Say: 'open notepad', 'close chrome', 'volume up', 'mute', 'lock system', 'search [topic]', or ask me anything!",
        }
        
        # Check for instant responses
        for key, response in instant_responses.items():
            if key in command_lower:
                return response
        
        # Pattern-based instant responses
        if any(word in command_lower for word in ["thank", "thanks", "appreciate"]):
            return "You're welcome! Happy to help."
        
        if any(word in command_lower for word in ["sorry", "apologize"]):
            return "No problem at all! Don't worry about it."
        
        if "tell me" in command_lower:
            if "about" in command_lower or "you" in command_lower:
                return "I'm Jarvis, an AI assistant that can answer questions, control your device, open applications, and help with tasks!"
            else:
                return "I'd be happy to help! Can you be more specific?"
        
        # Device control commands
        if "open " in command_lower:
            app = command_lower.replace("open ", "").strip()
            return f"Opening {app}..."
        
        if "close " in command_lower:
            app = command_lower.replace("close ", "").strip()
            return f"Closing {app}..."
        
        if any(word in command_lower for word in ["volume", "brightness", "mute", "shutdown", "restart", "lock", "sleep"]):
            return "Adjusting system settings..."
        
        # Use OpenRouter API for general queries
        if OPENROUTER_API_KEY:
            return self.get_ai_response(command)
        else:
            return f"Interesting point: '{command}'. (Set OPENROUTER_API_KEY for full AI capabilities!)"
    
    def get_ai_response(self, query):
        """Get response from OpenRouter AI API with better error handling"""
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Jarvis AI Assistant"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",  # Free model through OpenRouter
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Jarvis, a helpful and friendly AI assistant. Keep responses concise and under 100 words. You're integrated into a voice assistant, so be conversational and natural."
                    },
                    {
                        "role": "user",
                        "content": query
                    }
                ],
                "max_tokens": 150,
                "temperature": 0.7
            }
            
            response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "choices" in data and len(data["choices"]) > 0:
                    message = data["choices"][0]["message"]["content"].strip()
                    return message
                else:
                    print(f"API Response missing choices: {data}")
                    return "I got a response but it was incomplete. Please try again."
            
            else:
                # Log the actual error
                error_msg = response.text
                print(f"API Error {response.status_code}: {error_msg}")
                
                # Return user-friendly message with hint
                if response.status_code == 401:
                    return "API Key issue. Please get a new key from openrouter.ai and update it in the code."
                elif response.status_code == 429:
                    return "Rate limited. Please wait a moment before trying again."
                elif response.status_code == 500:
                    return "OpenRouter API is having issues. Please try again in a moment."
                else:
                    return f"API error {response.status_code}. Please try rephrasing your question."
        
        except requests.exceptions.Timeout:
            print("Request timeout")
            return "The request timed out. Please try again with a simpler question."
        except requests.exceptions.ConnectionError:
            print("Connection error")
            return "Unable to connect to the AI service. Please check your internet connection."
        except Exception as e:
            print(f"API Error: {e}")
            return f"I encountered an error: {str(e)[:50]}. Please try rephrasing your question."
    
    def execute_action(self, command):
        """Execute action commands including device control"""
        command_lower = command.lower()
        
        # Time command
        if "time" in command_lower and "what" in command_lower:
            now = datetime.datetime.now().strftime("%I:%M %p")
            response = f"The current time is {now}"
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            self.speak_response(response)
            return
        
        # Date command
        if "date" in command_lower and ("what" in command_lower or "today" in command_lower):
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            response = f"Today is {today}"
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            self.speak_response(response)
            return
        
        # Search command
        if "search" in command_lower and "wikipedia" not in command_lower:
            parts = command_lower.split("search ", 1)
            if len(parts) > 1:
                query = parts[1]
                webbrowser.open(f"https://google.com/search?q={query.replace(' ', '+')}")
                response = f"Searching Google for '{query}'..."
                self.root.after(0, lambda: self.add_message("Jarvis", response))
            return
        
        # Open YouTube
        if "youtube" in command_lower:
            webbrowser.open("https://youtube.com")
            response = "Opening YouTube..."
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            return
        
        # Open Google
        if "open google" in command_lower or "google" in command_lower:
            webbrowser.open("https://google.com")
            response = "Opening Google..."
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            return
        
        # Wikipedia search
        if "wikipedia" in command_lower:
            parts = command_lower.split("wikipedia ", 1)
            if len(parts) > 1:
                topic = parts[1]
                webbrowser.open(f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}")
                response = f"Searching Wikipedia for '{topic}'..."
            else:
                response = "What would you like to search on Wikipedia?"
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            return
        
        # Open Application
        if "open " in command_lower:
            app_name = command_lower.replace("open ", "").strip()
            response = open_application(app_name)
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            self.speak_response(response)
            return
        
        # Close Application
        if "close " in command_lower:
            app_name = command_lower.replace("close ", "").strip()
            response = close_application(app_name)
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            self.speak_response(response)
            return
        
        # WhatsApp message
        if "whatsapp" in command_lower and "send" in command_lower:
            response = "WhatsApp messaging requires manual authentication. Please open WhatsApp Web and try again."
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            self.speak_response(response)
            return
        
        # System Control
        if any(word in command_lower for word in ["volume", "mute", "shutdown", "restart", "lock", "sleep", "brightness"]):
            response = control_system(command)
            self.root.after(0, lambda: self.add_message("Jarvis", response))
            self.speak_response(response)
            return
    
    def speak_response(self, text):
        """Speak the response with improved error handling and retries"""
        if not hasattr(self, 'voice_output_state'):
            self.voice_output_state = True
        
        if not self.voice_output_state:
            return
        
        try:
            if engine is None:
                print("Voice engine not available")
                return
            
            # Limit text length and clean it
            text_to_speak = text[:500] if text else ""
            if not text_to_speak:
                return
            
            # Clean text for better speech
            text_to_speak = text_to_speak.replace("\n", " ").replace("  ", " ").strip()
            
            # Run speech in separate thread to avoid blocking UI
            def speak_thread(retry_count=0):
                try:
                    if engine and text_to_speak:
                        print(f"🔊 Speaking: {text_to_speak[:50]}...")
                        engine.say(text_to_speak)
                        engine.runAndWait()
                        print("✓ Speech completed")
                except RuntimeError as e:
                    if "run loop already started" in str(e):
                        # Known pyttsx3 issue - just skip
                        print(f"⚠ Voice output skipped (engine busy)")
                    else:
                        raise
                except Exception as e:
                    print(f"Voice playback error: {e}")
                    # Retry once on failure
                    if retry_count < 1 and "run loop" not in str(e):
                        print("Retrying speech...")
                        time.sleep(0.5)
                        speak_thread(retry_count + 1)
            
            thread = threading.Thread(target=speak_thread, daemon=True)
            thread.start()
        except Exception as e:
            print(f"Error in speak_response: {e}")
    
    def toggle_voice_output(self):
        """Toggle voice output on/off"""
        self.voice_output_state = not self.voice_output_state
        
        if self.voice_output_state:
            self.voice_output_btn.config(text="🔊 Voice ON", bg="#10a37f")
            self.add_message("System", "🔊 Voice output enabled ✓")
            print("✓ Voice output enabled")
        else:
            self.voice_output_btn.config(text="🔇 Voice OFF", bg="#666666")
            self.add_message("System", "🔇 Voice output disabled")
            print("✓ Voice output disabled")
    
    def set_voice_speed(self, speed):
        """Set voice playback speed"""
        global engine
        try:
            if engine:
                # Speed range: 50-300 (normal is ~150)
                engine.setProperty("rate", int(speed))
                print(f"✓ Voice speed set to: {speed}")
        except Exception as e:
            print(f"Error setting voice speed: {e}")
    
    def clear_chat(self):
        """Clear chat history"""
        # Save current chat if it has messages
        if self.conversation_history and len(self.conversation_history) > 1:  # More than just greeting
            self.add_chat_to_history()
        
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.conversation_history = []
        self.show_welcome_prompts()


def authenticate_user():
    """Open authentication window and return account manager"""
    def auth_callback(account_manager):
        nonlocal result
        result = account_manager
    
    result = None
    auth_window = AuthenticationWindow(auth_callback)
    auth_window.run()
    return result


def main():
    """Main function"""
    # Show authentication window
    account_manager = authenticate_user()
    
    # Create main GUI
    root = tk.Tk()
    gui = JarvisGUI(root, account_manager)
    root.mainloop()

if __name__ == "__main__":
    main()
