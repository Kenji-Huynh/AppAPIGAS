# settings_module.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class SettingsModule:
    """Handles application settings and configuration"""
    
    def __init__(self, parent_frame, api_manager, voice_manager, status_callback):
        self.parent = parent_frame
        self.api_manager = api_manager
        self.voice_manager = voice_manager
        self.update_status = status_callback
        
        # Create UI components
        self.create_widgets()
    
    def create_widgets(self):
        # Main settings container
        settings_container = ttk.Frame(self.parent)
        settings_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # API Settings
        api_frame = ttk.LabelFrame(settings_container, text="Cài đặt API")
        api_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # API Key field
        api_key_frame = ttk.Frame(api_frame)
        api_key_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(api_key_frame, text="API Key:").pack(side=tk.LEFT, padx=(0, 5))
        self.api_key_entry = ttk.Entry(api_key_frame, show="*", width=40)
        self.api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Populate field if API key exists
        if self.api_manager.api_key:
            self.api_key_entry.insert(0, self.api_manager.api_key)
        
        # Show/hide password
        self.show_password_var = tk.BooleanVar()
        ttk.Checkbutton(api_key_frame, text="Hiển thị", variable=self.show_password_var, 
                       command=self.toggle_password_visibility).pack(side=tk.LEFT, padx=5)
        
        # Save API key button
        ttk.Button(api_key_frame, text="Lưu API Key", 
                  command=self.save_api_key).pack(side=tk.LEFT, padx=5)
        
        # Test API button
        ttk.Button(api_key_frame, text="Kiểm tra API", 
                  command=self.test_api).pack(side=tk.LEFT, padx=5)
        
        # Model selection frame
        model_frame = ttk.Frame(api_frame)
        model_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(model_frame, text="Chọn Model:").pack(side=tk.LEFT, padx=(0, 5))
        self.model_combo = ttk.Combobox(model_frame, state="readonly", width=30)
        self.model_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Default models
        default_models = ['gemini-2.0-flash', 'gemini-1.5-flash']
        self.model_combo['values'] = default_models
        self.model_combo.set(self.api_manager.selected_model)
        
        # Refresh models button
        ttk.Button(model_frame, text="Làm mới danh sách", 
                  command=self.refresh_models).pack(side=tk.LEFT, padx=5)
        
        # Button to apply model selection
        ttk.Button(model_frame, text="Áp dụng", 
                  command=self.apply_model).pack(side=tk.LEFT, padx=5)
        
        # Voice Settings
        voice_frame = ttk.LabelFrame(settings_container, text="Cài đặt giọng nói")
        voice_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Voice selection frames
        voice_selection_frame = ttk.Frame(voice_frame)
        voice_selection_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Language selection
        ttk.Label(voice_selection_frame, text="Ngôn ngữ:").pack(side=tk.LEFT, padx=(0, 5))
        self.language_combo = ttk.Combobox(voice_selection_frame, state="readonly", width=15)
        self.language_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        # Get available languages
        available_languages = list(self.voice_manager.voice_data.keys())
        self.language_combo['values'] = available_languages
        self.language_combo.set(available_languages[0])
        self.language_combo.bind("<<ComboboxSelected>>", self.update_gender_options)
        
        # Gender selection
        ttk.Label(voice_selection_frame, text="Giới tính:").pack(side=tk.LEFT, padx=(10, 5))
        self.gender_combo = ttk.Combobox(voice_selection_frame, state="readonly", width=10)
        self.gender_combo.pack(side=tk.LEFT, padx=(0, 5))
        self.gender_combo['values'] = ["Male", "Female"]
        self.gender_combo.set("Male")
        self.gender_combo.bind("<<ComboboxSelected>>", self.update_voice_options)
        
        # Voice selection
        ttk.Label(voice_selection_frame, text="Giọng:").pack(side=tk.LEFT, padx=(10, 5))
        self.voice_combo = ttk.Combobox(voice_selection_frame, state="readonly", width=20)
        self.voice_combo.pack(side=tk.LEFT, padx=(0, 5))
        
        # Initialize voice dropdown
        self.update_gender_options(None)
        
        # Speed settings
        speed_frame = ttk.Frame(voice_frame)
        speed_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(speed_frame, text="Tốc độ:").pack(side=tk.LEFT, padx=(0, 5))
        self.speed_var = tk.IntVar(value=self.voice_manager.rate)
        speed_scale = ttk.Scale(speed_frame, from_=100, to=300, 
                               variable=self.speed_var, orient=tk.HORIZONTAL)
        speed_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        speed_label = ttk.Label(speed_frame, textvariable=self.speed_var, width=3)
        speed_label.pack(side=tk.LEFT)
        
        # Test voice button
        ttk.Button(speed_frame, text="Kiểm tra giọng", 
                  command=self.test_voice).pack(side=tk.RIGHT, padx=5)
        
        # Apply voice settings button
        ttk.Button(speed_frame, text="Áp dụng cài đặt", 
                  command=self.apply_voice_settings).pack(side=tk.RIGHT, padx=5)
        
        # About section
        about_frame = ttk.LabelFrame(settings_container, text="Thông tin")
        about_frame.pack(fill=tk.X, padx=5, pady=5)
        
        about_text = "AI Assistant v1.0\n"
        about_text += "Phát triển bởi: Hoàng Thịnh\n"
        about_text += "Sử dụng API: Google AI Studio\n"
        
        about_label = ttk.Label(about_frame, text=about_text, justify=tk.LEFT)
        about_label.pack(padx=10, pady=10)
    
    def toggle_password_visibility(self):
        """Toggle API key visibility"""
        if self.show_password_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
    
    def save_api_key(self):
        """Save API key to environment"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập API key")
            return
        
        success, message = self.api_manager.save_api_key(api_key)
        if success:
            messagebox.showinfo("Thành công", message)
            self.update_status("API key đã lưu", "green")
        else:
            messagebox.showerror("Lỗi", message)
            self.update_status("Lỗi lưu API key", "red")
    
    def test_api(self):
        """Test API key validity"""
        api_key = self.api_key_entry.get().strip()
        if not api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập API key")
            return
        
        # Show testing status
        self.update_status("Đang kiểm tra API...", "orange")
        
        def test():
            # Save temporarily for testing
            old_key = self.api_manager.api_key
            self.api_manager.api_key = api_key
            self.api_manager.configure_api()
            
            try:
                # Try to list models as a test
                success, message, _ = self.api_manager.get_available_models()
                
                # Restore original key if test failed
                if not success:
                    self.api_manager.api_key = old_key
                    self.api_manager.configure_api()
                
                # Update UI from main thread
                self.parent.after(0, lambda: self.show_test_result(success, message))
            except Exception as e:
                # Restore original key
                self.api_manager.api_key = old_key
                self.api_manager.configure_api()
                
                # Show error
                self.parent.after(0, lambda: self.show_test_result(False, str(e)))
        
        # Run in background thread
        thread = threading.Thread(target=test)
        thread.daemon = True
        thread.start()
    
    def show_test_result(self, success, message):
        """Show API test results"""
        if success:
            messagebox.showinfo("Kiểm tra API", "API key hợp lệ")
            self.update_status("API key hợp lệ", "green")
        else:
            messagebox.showerror("Kiểm tra API", f"API key không hợp lệ: {message}")
            self.update_status("API key không hợp lệ", "red")
    
    def refresh_models(self):
        """Refresh available models from API"""
        if not self.api_manager.api_key:
            messagebox.showwarning("Cảnh báo", "Vui lòng cấu hình API key trước")
            return
        
        # Show loading status
        self.update_status("Đang tải danh sách model...", "orange")
        
        def load_models():
            try:
                success, message, models = self.api_manager.get_available_models()
                
                # Update UI from main thread
                self.parent.after(0, lambda: self.update_model_list(success, message, models))
            except Exception as e:
                self.parent.after(0, lambda: self.update_model_list(False, str(e), []))
        
        # Run in background thread
        thread = threading.Thread(target=load_models)
        thread.daemon = True
        thread.start()
    
    def update_model_list(self, success, message, models):
        """Update model dropdown with available models"""
        if success:
            self.model_combo['values'] = models
            messagebox.showinfo("Thành công", "Đã cập nhật danh sách model")
            self.update_status("Sẵn sàng", "green")
        else:
            messagebox.showerror("Lỗi", message)
            self.update_status("Lỗi tải model", "red")
    
    def apply_model(self):
        """Apply selected model"""
        model = self.model_combo.get()
        if model:
            self.api_manager.set_model(model)
            messagebox.showinfo("Thành công", f"Đã chọn model: {model}")
    
    def update_gender_options(self, event):
        """Update gender dropdown based on language selection"""
        language = self.language_combo.get()
        if language:
            # Get available genders for this language
            available_genders = []
            for gender in self.voice_manager.voice_data[language]:
                if self.voice_manager.voice_data[language][gender]:
                    available_genders.append(gender)
            
            self.gender_combo['values'] = available_genders
            if available_genders:
                self.gender_combo.set(available_genders[0])
                self.update_voice_options(None)
    
    def update_voice_options(self, event):
        """Update voice dropdown based on language and gender selection"""
        language = self.language_combo.get()
        gender = self.gender_combo.get()
        
        if language and gender:
            voices = self.voice_manager.voice_data[language][gender]
            self.voice_combo['values'] = [v.name for v in voices]
            if voices:
                self.voice_combo.set(voices[0].name)
    
    def test_voice(self):
        """Test selected voice and settings"""
        # Get selected voice
        language = self.language_combo.get()
        gender = self.gender_combo.get()
        voice_name = self.voice_combo.get()
        
        if not voice_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giọng trước")
            return
        
        # Find voice ID from name
        selected_voice = None
        for voice in self.voice_manager.voice_data[language][gender]:
            if voice.name == voice_name:
                selected_voice = voice
                break
        
        if not selected_voice:
            messagebox.showerror("Lỗi", "Không tìm thấy giọng đã chọn")
            return
        
        # Store current settings to restore later
        current_voice = self.voice_manager.current_voice_id
        current_rate = self.voice_manager.rate
        
        # Apply test settings
        self.voice_manager.set_voice(selected_voice.id)
        self.voice_manager.set_rate(self.speed_var.get())
        
        # Speak test phrase
        test_text = "Xin chào, đây là bài kiểm tra giọng nói."
        self.voice_manager.speak(test_text)
        
        # Restore previous settings
        self.voice_manager.set_voice(current_voice)
        self.voice_manager.set_rate(current_rate)
    
    def apply_voice_settings(self):
        """Apply voice settings"""
        # Get selected voice
        language = self.language_combo.get()
        gender = self.gender_combo.get()
        voice_name = self.voice_combo.get()
        
        if not voice_name:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn giọng trước")
            return
        
        # Find voice ID from name
        selected_voice = None
        for voice in self.voice_manager.voice_data[language][gender]:
            if voice.name == voice_name:
                selected_voice = voice
                break
        
        if not selected_voice:
            messagebox.showerror("Lỗi", "Không tìm thấy giọng đã chọn")
            return
        
        # Apply settings
        self.voice_manager.set_voice(selected_voice.id)
        self.voice_manager.set_rate(self.speed_var.get())
        
        messagebox.showinfo("Thành công", "Đã áp dụng cài đặt giọng nói")

