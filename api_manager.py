# api_manager.py
import os
import google.generativeai as genai
from dotenv import load_dotenv, set_key

class APIManager:
    """Manages API authentication and model selection"""
    
    def __init__(self):
        self.api_key = None
        self.selected_model = 'gemini-2.0-flash'  # Default model
        self.load_api_key_from_env()
    
    def load_api_key_from_env(self):
        """Load API key from .env file if it exists"""
        try:
            load_dotenv()
            self.api_key = os.getenv('GEMINI_API_KEY')
            
            # Configure genai if API key exists
            if self.api_key:
                self.configure_api()
        except Exception as e:
            print(f"Error loading API key: {str(e)}")
    
    def configure_api(self):
        """Configure the Gemini API with current settings"""
        genai.configure(api_key=self.api_key, transport="rest")
    
    def save_api_key(self, api_key):
        """Save API key to environment and .env file"""
        self.api_key = api_key
        self.configure_api()
        
        try:
            # Check if .env file exists
            env_exists = os.path.exists('.env')
            
            # Create new file or update existing one
            if not env_exists:
                with open('.env', 'w') as f:
                    f.write(f"GEMINI_API_KEY={api_key}\n")
            else:
                set_key('.env', 'GEMINI_API_KEY', api_key)
            
            return True, "Saved API key successfully"
        except Exception as e:
            return False, f"Error saving API key: {str(e)}"
    
    def set_model(self, model_name):
        """Set the active model"""
        self.selected_model = model_name
    
    def get_available_models(self):
        """Get list of available models from API"""
        if not self.api_key:
            return False, "API key not configured", []
            
        try:
            self.configure_api()
            model_list = genai.list_models()
            model_names = [model.name for model in model_list]
            return True, "Models retrieved successfully", model_names
        except Exception as e:
            return False, f"Error retrieving models: {str(e)}", []
    
    def get_model(self):
        """Get a configured GenerativeModel instance"""
        if not self.api_key:
            raise ValueError("API key not configured")
        
        return genai.GenerativeModel(model_name=self.selected_model)

