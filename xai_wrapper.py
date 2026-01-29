import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class XAIClient:
    def __init__(self):
        self.api_key = os.getenv("XAI_API_KEY")
        self.api_url = "https://api.x.ai/v1/chat/completions"
        if not self.api_key:
            raise ValueError("XAI_API_KEY not found in .env")

    def generate_content(self, system_prompt, user_prompt):
        """
        Generates content using xAI Grok model.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "grok-4-1-fast-reasoning", # Updated to the precise identifier found in the API model list
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 500
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"xAI API Error: {e}")
            if 'response' in locals() and hasattr(response, 'text'):
                 print(f"Response Body: {response.text}")
            return None
