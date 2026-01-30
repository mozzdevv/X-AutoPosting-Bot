import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class XAIWrapper:
    """
    Wrapper for xAI (Grok) API interactions.
    Compatible with the updated agents.py interface.
    """
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        self.api_url = "https://api.x.ai/v1/chat/completions"
        if not self.api_key:
            raise ValueError("XAI_API_KEY not found in .env")

    def generate_completion(self, prompt, system_prompt="You are a helpful AI assistant."):
        """
        Generates a completion for the given prompt using xAI Grok model.
        
        Args:
            prompt (str): The user's input prompt
            system_prompt (str): Optional system instruction
            
        Returns:
            str: The model's response text
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "grok-2-latest",  # Using a reliable model identifier
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "stream": False
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            
            if response.status_code != 200:
                print(f"⚠️ xAI API Error {response.status_code}: {response.text}")
                return None
                
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"⚠️ Unexpected API response format: {result}")
                return None
                
        except Exception as e:
            print(f"❌ xAI Request Exception: {e}")
            return None
