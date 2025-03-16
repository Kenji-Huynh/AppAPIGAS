# summarizer_module.py
import textwrap
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading

class SummarizerModule:
    """Handles text summarization functionality"""
    
    def __init__(self, parent_frame, api_manager, web_scraper, voice_manager, status_callback):
        self.parent = parent_frame
        self.api_manager = api_manager
        self.web_scraper = web_scraper
        self.voice_manager = voice_manager
        self.update_status = status_callback
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        # Frame for input
        input_frame = ttk.LabelFrame(self.parent, text="Nhập URL hoặc văn bản")
        input_frame.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # Text area for input
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Frame for controls
        control_frame = ttk.Frame(self.parent)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # URL quick input
        url_frame = ttk.Frame(control_frame)
        url_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Label(url_frame, text="URL nhanh:").pack(side=tk.LEFT, padx=(0, 5))
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        url_load_btn = ttk.Button(url_frame, text="Tải URL", command=self.load_url)
        url_load_btn.pack(side=tk.LEFT)
        
        # Buttons frame
        buttons_frame = ttk.Frame(control_frame)
        buttons_frame.pack(side=tk.RIGHT, padx=5)
        
        # Summarize button
        self.summarize_btn = ttk.Button(buttons_frame, text="Tóm tắt", command=self.summarize)
        self.summarize_btn.pack(side=tk.LEFT, padx=5)
        
        # Load file button
        self.load_file_btn = ttk.Button(buttons_frame, text="Tải file", command=self.load_file)
        self.load_file_btn.pack(side=tk.LEFT, padx=5)
        
        # Read summary button
        self.speak_summary_btn = ttk.Button(buttons_frame, text="Đọc bản tóm tắt", 
                                          command=lambda: self.voice_manager.speak(self.output_text.get("1.0", tk.END)))
        self.speak_summary_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress indicator
        self.progress_frame = ttk.Frame(self.parent)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode="indeterminate")
        
        # Frame for output
        output_frame = ttk.LabelFrame(self.parent, text="Bản tóm tắt")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text area for output
        self.output_text = scrolledtext.ScrolledText(output_frame, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def load_url(self):
        """Load content from URL in quick URL field"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập URL")
            return
            
        try:
            self.url_entry.config(state=tk.DISABLED)
            self.update_status("Đang tải URL...", "orange")
            
            # Use threading to avoid freezing UI
            def fetch_url():
                success, result = self.web_scraper.get_text_from_url(url)
                
                if success:
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, result)
                    messagebox.showinfo("Thành công", "Đã tải nội dung từ URL")
                else:
                    messagebox.showerror("Lỗi", result)
                
                self.url_entry.config(state=tk.NORMAL)
                self.update_status("Sẵn sàng", "green")
            
            thread = threading.Thread(target=fetch_url)
            thread.daemon = True
            thread.start()
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải nội dung từ URL: {str(e)}")
            self.url_entry.config(state=tk.NORMAL)
            self.update_status("Lỗi", "red")
    
    def load_file(self):
        """Load content from a text file"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể đọc file: {str(e)}")
    
    def summarize_text(self, text):
        """Generate summary using AI API"""
        try:
            if not self.api_manager.api_key:
                return False, "Vui lòng cấu hình API key trước"
            
            model = self.api_manager.get_model()
            prompt = f"""Tóm tắt văn bản sau một cách ngắn gọn nhưng đầy đủ ý chính:

{text}

Tóm tắt:"""
            response = model.generate_content(prompt)
            return True, response.text
        except Exception as e:
            return False, f"Lỗi khi tóm tắt: {str(e)}"
    
    def process_input(self, input_text):
        """Process input text or URL"""
        if self.web_scraper.is_url(input_text):
            success, text = self.web_scraper.get_text_from_url(input_text)
            if success:
                return self.summarize_text(text)
            else:
                return False, text
        else:
            return self.summarize_text(input_text)
    
    def summarize(self):
        """Handle the summarization process"""
        input_data = self.input_text.get("1.0", tk.END).strip()
        if not input_data:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập văn bản hoặc URL để tóm tắt")
            return
        
        # Disable controls during processing
        self.summarize_btn.config(state=tk.DISABLED)
        self.load_file_btn.config(state=tk.DISABLED)
        self.input_text.config(state=tk.DISABLED)
        
        # Show progress bar
        self.progress_bar.pack(fill=tk.X, expand=True)
        self.progress_bar.start()
        self.update_status("Đang tóm tắt...", "orange")
        
        # Process in a separate thread to avoid freezing UI
        def process():
            success, result = self.process_input(input_data)
            
            # Update UI from the main thread
            self.parent.after(0, lambda: self.update_results(success, result))
        
        thread = threading.Thread(target=process)
        thread.daemon = True
        thread.start()
    
    def update_results(self, success, result):
        """Update UI with summarization results"""
        # Stop progress indication
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        
        # Re-enable controls
        self.summarize_btn.config(state=tk.NORMAL)
        self.load_file_btn.config(state=tk.NORMAL)
        self.input_text.config(state=tk.NORMAL)
        
        if success:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)
            self.update_status("Tóm tắt thành công", "green")
        else:
            messagebox.showerror("Lỗi", result)
            self.update_status("Tóm tắt thất bại", "red")
