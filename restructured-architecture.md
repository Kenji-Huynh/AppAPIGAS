# Proposed Architecture for AI Assistant App

## Core Modules

### 1. Main Application
- `AIAssistantApp` - Entry point and UI coordinator

### 2. UI Components
- `ModernUI` - Styling class (already separate)
- `UIFactory` - New class to handle widget creation

### 3. Functional Modules
- `SummarizerModule` - Text summarization functionality
- `ChatModule` - Chat interface and logic
- `TTSModule` - Text-to-speech system
- `SettingsModule` - Application configuration

### 4. Utility Classes
- `APIManager` - API key and model management
- `WebScraper` - URL content extraction
- `VoiceManager` - Voice categorization and selection
