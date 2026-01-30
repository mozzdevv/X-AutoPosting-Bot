import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

class XHandler:
    def __init__(self):
        self.consumer_key = os.getenv("X_CONSUMER_KEY")
        self.consumer_secret = os.getenv("X_CONSUMER_SECRET")
        self.access_token = os.getenv("X_ACCESS_TOKEN")
        self.access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET")
        self.bearer_token = os.getenv("X_BEARER_TOKEN")
        
        self.client = None
        self._authenticate()

    def _authenticate(self):
        try:
            # For posting tweets (v2 API), we need Client with consumer/access tokens
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            print(f"X API Client Initialized (Consumer Key: {self.consumer_key[:5]}...)")
        except Exception as e:
            print(f"X API Authentication Failed: {e}")

    def post_tweet(self, text):
        """
        Posts a tweet to the account.
        """
        if not self.client:
            return {"status": "error", "message": "Client not authenticated"}
            
        try:
            response = self.client.create_tweet(text=text)
            return {"status": "success", "data": response.data}
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return {"status": "error", "message": str(e)}
    def search_dev_jokes(self):
        """
        Searches for viral dev/tech jokes on X.
        Uses keywords like 'programming humor', 'dev life', etc.
        """
        if not self.client:
            return []
            
        queries
