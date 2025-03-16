# tts_module.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading

class TTSModule:
    """Handles text-to-speech conversion"""
    
    def __init__(self, parent_frame, voice_manager, status_callback):
        self.parent = parent_frame
        self.voice_manager = voice_manager
        self.update_status = status_callback
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        # Main TTS container
        tts_container = ttk.Frame(self.parent)
        tts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text input area
        input_frame = ttk.LabelFrame(tts_container, text="Văn bản cần chuyển đổi")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Control panel
        control_frame = ttk.Frame(tts_container)
        control_frame.pack(fill=tk.X, expand=False, padx=5, pady=5)
        
        # Left side: text limit info
        info_frame = ttk.Frame(control_frame)
        info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.char_count_var = tk.StringVar(value="0 kí tự")
        char_count_label = ttk.Label(info_frame, textvariable=self.char_count_var)
        char_count_label.pack(side=tk.LEFT, padx=5)
        
        # Update character count when text changes
        self.text_input.bind("<<Modified>>", self.update_char_count)
        
        # Right side: buttons
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(side=tk.RIGHT)
        
        # Button to clear text
        ttk.Button(buttons_frame, text="Xóa", 
                  command=self.clear_text).pack(side=tk.LEFT, padx=5)
        
        # Button to convert to speech
        self.speak_btn = ttk.Button(buttons_frame, text="Đọc", 
                                  command=self.speak_text)
        self.speak_btn.pack(side=tk.LEFT, padx=5)
        
        # Button to stop speech
        self.stop_btn = ttk.Button(buttons_frame, text="Dừng", 
                                 command=self.stop_speech, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress indicator
        self.progress_frame = ttk.Frame(tts_container)
        self.progress_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(self.progress_frame, 
                                          variable=self.progress_var)
        
        # Extra options
        options_frame = ttk.LabelFrame(tts_container, text="Tùy chọn")
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Option to break text into chunks
        chunk_frame = ttk.Frame(options_frame)
        chunk_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.chunk_var = tk.BooleanVar(value=True)
        chunk_check = ttk.Checkbutton(chunk_frame, text="Chia văn bản thành đoạn", 
                                     variable=self.chunk_var)
        chunk_check.pack(side=tk.LEFT)
        
        ttk.Label(chunk_frame, text="Độ dài đoạn (kí tự):").pack(side=tk.LEFT, padx=(20, 5))
        
        self.chunk_size_var = tk.StringVar(value="250")
        chunk_size_entry = ttk.Entry(chunk_frame, textvariable=self.chunk_size_var, width=5)
        chunk_size_entry.pack(side=tk.LEFT)
        
        # Option to add pause between chunks
        pause_frame = ttk.Frame(options_frame)
        pause_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(pause_frame, text="Dừng giữa các đoạn (giây):").pack(side=tk.LEFT, padx=(0, 5))
        
        self.pause_var = tk.StringVar(value="1.0")
        pause_entry = ttk.Entry(pause_frame, textvariable=self.pause_var, width=5)
        pause_entry.pack(side=tk.LEFT)
    
    def update_char_count(self, event=None):
        """Update character count display"""
        if event:
            # Prevent infinite recursion
            self.text_input.edit_modified(False)
        
        text = self.text_input.get("1.0", tk.END)
        char_count = len(text) - 1  # Subtract 1 for the extra newline
        self.char_count_var.set(f"{char_count} kí tự")
    
    def clear_text(self):
        """Clear text input area"""
        self.text_input.delete("1.0", tk.END)
        self.update_char_count()
    
    def speak_text(self):
        """Convert text to speech"""
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản để chuyển đổi")
            return
        
        # Update UI state
        self.speak_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.text_input.config(state=tk.DISABLED)
        
        # Show progress bar
        self.progress_bar.pack(fill=tk.X, expand=True)
        self.update_status("Đang chuyển đổi...", "orange")
        
        # Process in separate thread
        self.active_thread = threading.Thread(target=self.process_speech, args=(text,))
        self.active_thread.daemon = True
        self.active_thread.start()
    
    def process_speech(self, text):
        """Process and speak text, possibly in chunks"""
        try:
            # Check if we should process in chunks
            if self.chunk_var.get():
                try:
                    chunk_size = int(self.chunk_size_var.get())
                    pause_duration = float(self.pause_var.get())
                except ValueError:
                    # Default values if parsing fails
                    chunk_size = 250
                    pause_duration = 1.0
                
                # Split text into chunks and process
                chunks = self.split_into_chunks(text, chunk_size)
                total_chunks = len(chunks)
                
                for i, chunk in enumerate(chunks):
                    # Check if stopped
                    if not hasattr(self, 'active_thread') or not self.active_thread:
                        break
                    
                    # Update progress
                    progress = (i / total_chunks) * 100
                    self.parent.after(0, lambda p=progress: self.update_progress(p))
                    
                    # Speak chunk
                    self.voice_manager.speak(chunk)
                    
                    # Pause between chunks
                    if i < total_chunks - 1:
                        import time
                        time.sleep(pause_duration)
            else:
                # Speak entire text at once
                self.voice_manager.speak(text)
            
            # Update UI from main thread
            self.parent.after(0, self.speech_complete)
            
        except Exception as e:
            # Handle errors on main thread
            self.parent.after(0, lambda: self.speech_error(str(e)))
    
    def split_into_chunks(self, text, chunk_size):
        """Split text into chunks of approximately chunk_size characters"""
        # Try to split at sentence boundaries
        sentences = []
        current = ""
        
        # Basic sentence splitting
        for part in text.replace(".", ".|").replace("!", "!|").replace("?", "?|").split("|"):
            if part:
                if len(current) + len(part) <= chunk_size:
                    current += part
                else:
                    if current:
                        sentences.append(current)
                    current = part
        
        if current:
            sentences.append(current)
        
        # If no sentence boundaries found, fallback to chunk_size
        if not sentences:
            sentences = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        return sentences
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_var.set(value)
    
    def speech_complete(self):
        """Handle completion of speech conversion"""
        # Reset UI state
        self.speak_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.text_input.config(state=tk.NORMAL)
        self.text_input.focus()
        
        # Hide progress
        self.progress_bar.pack_forget()
        self.progress_var.set(0)
        
        self.update_status("Chuyển đổi hoàn tất", "green")
        self.active_thread = None
    
    def speech_error(self, error_message):
        """Handle errors in speech conversion"""
        # Reset UI state
        self.speak_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.text_input.config(state=tk.NORMAL)
        
        # Hide progress
        self.progress_bar.pack_forget()
        self.progress_var.set(0)
        
        messagebox.showerror("Lỗi", f"Không thể chuyển đổi: {error_message}")
        self.update_status("Lỗi chuyển đổi", "red")
        self.active_thread = None
    
    def stop_speech(self):
        """Stop ongoing speech conversion"""
        # Clear active thread reference to signal stop
        self.active_thread = None
        
        # Stop TTS engine
        try:
            self.voice_manager.tts_engine.stop()
        except:
            pass
        
        # Reset UI state
        self.speak_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.text_input.config(state=tk.NORMAL)
        
        # Hide progress
        self.progress_bar.pack_forget()
        self.progress_var.set(0)
        
        self.update_status("Đã dừng", "orange")

