# web_scraper.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebScraper:
    """Handles web page content extraction"""
    
    @staticmethod
    def is_url(text):
        """Check if text is a valid URL"""
        try:
            result = urlparse(text)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def get_text_from_url(url):
        """Extract text content from URL"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to get main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            
            if main_content:
                text = ' '.join(main_content.stripped_strings)
            else:
                # Fallback to body content
                text = ' '.join(soup.body.stripped_strings)
                
            return True, text
        except requests.exceptions.RequestException as e:
            return False, f"Error loading URL: {str(e)}"

