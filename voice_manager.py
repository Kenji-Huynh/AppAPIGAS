# voice_manager.py
import pyttsx3

class VoiceManager:
    """Manages text-to-speech voices and settings"""
    
    def __init__(self):
        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        
        # Get available voices
        self.voices = self.tts_engine.getProperty('voices')
        
        # Current voice selections
        self.current_voice_id = self.voices[0].id if self.voices else None
        self.rate = 200  # Default speed
        
        # Categorized voices
        self.voice_data = self.categorize_voices()
    
    def categorize_voices(self):
        """Categorize available voices by language and gender"""
        voice_data = {
            "Vietnamese": {"Male": [], "Female": []},
            "English": {"Male": [], "Female": []},
            "Chinese": {"Male": [], "Female": []},
            "Japanese": {"Male": [], "Female": []},
            "Other": {"Male": [], "Female": []}
        }
        
        # Helper function to determine gender
        def predict_gender(voice_name):
            female_indicators = ['female', 'woman', 'girl', 'nữ']
            for indicator in female_indicators:
                if indicator in voice_name.lower():
                    return "Female"
            return "Male"  # Default to male if not specified
        
        for voice in self.voices:
            voice_name = voice.name.lower()
            gender = predict_gender(voice_name)
            
            # Categorize by language patterns
            if any(pattern in voice_name for pattern in ['vietnam', 'vi-vn']):
                voice_data["Vietnamese"][gender].append(voice)
            elif any(pattern in voice_name for pattern in ['en-us', 'en-gb', 'english']):
                voice_data["English"][gender].append(voice)
            elif any(pattern in voice_name for pattern in ['chinese', 'zh', 'cmn']):
                voice_data["Chinese"][gender].append(voice)
            elif any(pattern in voice_name for pattern in ['japan', 'jp', 'ja']):
                voice_data["Japanese"][gender].append(voice)
            else:
                voice_data["Other"][gender].append(voice)
        
        return voice_data
    
    def set_voice(self, voice_id):
        """Set the active voice"""
        self.current_voice_id = voice_id
    
    def set_rate(self, rate):
        """Set speech rate"""
        self.rate = rate
    
    def speak(self, text):
        """Convert text to speech"""
        if not text.strip():
            return False
            
        try:
            # Configure engine
            self.tts_engine.setProperty('rate', self.rate)
            
            if self.current_voice_id:
                self.tts_engine.setProperty('voice', self.current_voice_id)
            
            # Perform speech
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"TTS error: {str(e)}")
            return False
