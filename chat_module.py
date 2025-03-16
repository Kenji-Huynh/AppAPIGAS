# chat_module.py
import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

class ChatModule:
    """Handles chat interface and conversation logic"""
    
    def __init__(self, parent_frame, api_manager, voice_manager, status_callback):
        self.parent = parent_frame
        self.api_manager = api_manager
        self.voice_manager = voice_manager
        self.update_status = status_callback
        
        # Chat history
        self.chat_history = []
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        # Main chat container
        self.chat_container = ttk.Frame(self.parent)
        self.chat_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat display area
        chat_display_frame = ttk.LabelFrame(self.chat_container, text="Cuộc trò chuyện")
        chat_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(chat_display_frame, wrap=tk.WORD)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.config(state=tk.DISABLED)
        
        # Input area
        input_frame = ttk.Frame(self.chat_container)
        input_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        self.chat_input = ttk.Entry(input_frame)
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        self.chat_input.bind("<Return>", lambda e: self.send_message())
        
        # Chat buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        self.send_btn = ttk.Button(buttons_frame, text="Gửi", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=5)
        
        self.voice_btn = ttk.Button(buttons_frame, text="Đọc phản hồi", 
                                   command=self.read_last_response)
        self.voice_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = ttk.Button(buttons_frame, text="Xóa", command=self.clear_chat)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress indicator
        self.progress_frame = ttk.Frame(self.chat_container)
        self.progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode="indeterminate")
    
    def append_message(self, message, sender):
        """Add a message to the chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add spacing between messages
        if self.chat_history:
            self.chat_display.insert(tk.END, "\n\n")
        
        # Format differently based on sender
        if sender == "user":
            self.chat_display.insert(tk.END, "Bạn: ", "user_tag")
            self.chat_history.append({"role": "user", "content": message})
        else:
            self.chat_display.insert(tk.END, "AI: ", "ai_tag")
            self.chat_history.append({"role": "assistant", "content": message})
        
        # Add the message
        self.chat_display.insert(tk.END, message)
        
        # Apply tags for styling
        self.chat_display.tag_configure("user_tag", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("ai_tag", foreground="green", font=("Arial", 10, "bold"))
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Send user message to the AI and get response"""
        message = self.chat_input.get().strip()
        if not message:
            return
        
        # Clear input field
        self.chat_input.delete(0, tk.END)
        
        # Add user message to chat
        self.append_message(message, "user")
        
        # Disable input during processing
        self.chat_input.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        
        # Show progress
        self.progress_bar.pack(fill=tk.X, expand=True)
        self.progress_bar.start()
        self.update_status("Đang xử lý...", "orange")
        
        # Process in background thread
        def get_ai_response():
            try:
                response = self.query_model(message)
                
                # Schedule UI update on main thread
                self.parent.after(0, lambda: self.handle_response(response))
            except Exception as e:
                self.parent.after(0, lambda: self.handle_error(str(e)))
        
        thread = threading.Thread(target=get_ai_response)
        thread.daemon = True
        thread.start()
    
    def query_model(self, message):
        """Send query to the AI model"""
        if not self.api_manager.api_key:
            raise ValueError("API key not configured")
        
        model = self.api_manager.get_model()
        
        # Convert chat history to Gemini's expected format
        formatted_history = []
        for item in self.chat_history[-10:]:
            if item["role"] == "user":
                formatted_history.append({"role": "user", "parts": [{"text": item["content"]}]})
            elif item["role"] == "assistant":
                formatted_history.append({"role": "model", "parts": [{"text": item["content"]}]})
        
        # Add current message
        formatted_history.append({"role": "user", "parts": [{"text": message}]})
        
        # Generate response
        response = model.generate_content(formatted_history)
        return response.text
    
    def handle_response(self, response):
        """Process AI response and update UI"""
        # Stop progress
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        # Add response to chat
        self.append_message(response, "assistant")
        
        # Re-enable input
        self.chat_input.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        self.chat_input.focus()
        
        self.update_status("Sẵn sàng", "green")
    
    def handle_error(self, error_message):
        """Handle API errors"""
        # Stop progress
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        # Add error as system message
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\n\nHệ thống: Lỗi - " + error_message, "error_tag")
        self.chat_display.tag_configure("error_tag", foreground="red", font=("Arial", 10, "italic"))
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Re-enable input
        self.chat_input.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        
        self.update_status("Lỗi", "red")
    
    def read_last_response(self):
        """Read the last AI response using TTS"""
        if not self.chat_history:
            return
            
        # Find last assistant message
        for message in reversed(self.chat_history):
            if message["role"] == "assistant":
                self.voice_manager.speak(message["content"])
                break
    
    def clear_chat(self):
        """Clear the chat history and display"""
        self.chat_history = []
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
