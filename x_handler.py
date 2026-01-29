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
            
        queries = [
            "programming humor -is:retweet lang:en",
            "developer joke -is:retweet lang:en",
            "\"software engineering\" humor -is:retweet lang:en",
            "from:ThePrimeagen humor",
            "from:levelsio dev"
        ]
        
        viral_tweets = []
        try:
            # We search for the first query in this example for simplicity
            # but we could cycle through them
            query = random.choice(queries)
            response = self.client.search_recent_tweets(
                query=query, 
                max_results=10,
                tweet_fields=['public_metrics', 'text']
            )
            
            if response.data:
                for tweet in response.data:
                    # Clean the text (remove URLs/mentions if needed)
                    text = tweet.text
                    viral_tweets.append(text)
                    
            print(f"Sensed {len(viral_tweets)} viral dev jokes on X.")
            return viral_tweets
        except Exception as e:
            print(f"Error sensing viral trends: {e}")
            return []

import random # Ensure random is available in this module
