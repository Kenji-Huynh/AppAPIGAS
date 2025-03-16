# app.py
import tkinter as tk
from tkinter import ttk
import sys
import os

# Import custom modules
from api_manager import APIManager
from voice_manager import VoiceManager
from web_scraper import WebScraper
from summarizer_module import SummarizerModule
from chat_module import ChatModule
from tts_module import TTSModule
from settings_module import SettingsModule
from ui_factory import UIFactory

class AIAssistantApp:
    """Main application class for AI Assistant"""
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        
        # Initialize utility managers
        self.api_manager = APIManager()
        self.voice_manager = VoiceManager()
        self.web_scraper = WebScraper()
        
        # Create UI
        self.create_ui()
        
        # Initialize modules with dependency injection
        self.init_modules()
        
        # Check API key on startup
        self.check_api_key()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Vietnamese AI Assistant")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use a more modern theme
        
        # Add custom styles if needed
        #self.style.configure('TButton', font=('Arial', 10))
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def create_ui(self):
        """Create the main UI components"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create and configure the main notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.tabs = {
            "summarizer": UIFactory.create_tab(self.notebook, "Tóm tắt văn bản"),
            "chat": UIFactory.create_tab(self.notebook, "Chat với AI"),
            "tts": UIFactory.create_tab(self.notebook, "Chuyển văn bản thành giọng nói"),
            "settings": UIFactory.create_tab(self.notebook, "Cài đặt")
        }
        
        # Status bar at the bottom
        self.status_label = UIFactory.create_status_bar(self.root)
        self.update_status("Khởi động ứng dụng...", "blue")
    
    def init_modules(self):
        """Initialize all functional modules"""
        # Create modules with dependencies injected
        self.summarizer = SummarizerModule(
            self.tabs["summarizer"], 
            self.api_manager, 
            self.web_scraper, 
            self.voice_manager, 
            self.update_status
        )
        
        self.chat = ChatModule(
            self.tabs["chat"], 
            self.api_manager,
            self.voice_manager,
            self.update_status
        )
        
        self.tts = TTSModule(
            self.tabs["tts"],
            self.voice_manager,
            self.update_status
        )
        
        self.settings = SettingsModule(
            self.tabs["settings"],
            self.api_manager,
            self.voice_manager,
            self.update_status
        )
    
    def check_api_key(self):
        """Check if API key is configured on startup"""
        if not self.api_manager.api_key:
            self.update_status("API key chưa được cấu hình", "orange")
            # Switch to settings tab
            self.notebook.select(self.tabs["settings"])
        else:
            self.update_status("Sẵn sàng", "green")
    
    def update_status(self, message, color="black"):
        """Update status bar with message and color"""
        self.status_label.config(text=message, foreground=color)
    
    def on_close(self):
        """Handle application closing"""
        # Clean up resources
        try:
            # Stop any ongoing TTS
            self.voice_manager.tts_engine.stop()
        except:
            pass
        
        # Close application
        self.root.destroy()
        sys.exit()

# Run application
if __name__ == "__main__":
    root = tk.Tk()
    app = AIAssistantApp(root)
    root.mainloop()