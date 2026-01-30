"""
Updated X Handler with enhanced trend fetching for tech topics
Handles posting to X and fetching trending tech topics
"""

import os
import tweepy
import random
from dotenv import load_dotenv

load_dotenv()


class XHandler:
    """
    Handles all interactions with X (Twitter) API
    - Posting tweets
    - Fetching trending topics
    - Managing authentication
    """
    
    def __init__(self):
        """Initialize X API client with credentials from .env"""
        self.bearer_token = os.getenv('X_BEARER_TOKEN')
        self.api_key = os.getenv('X_API_KEY')
        self.api_secret = os.getenv('X_API_SECRET')
        self.access_token = os.getenv('X_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
        
        # Initialize Tweepy client for v2 API
        self.client = tweepy.Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_token_secret
        )
        
        print("✅ X Handler initialized successfully")
    
    def post_tweet(self, text):
        """
        Post a tweet to X
        
        Args:
            text (str): Tweet content (max 280 chars)
            
        Returns:
            str: URL to the posted tweet, or None if failed
        """
        try:
            # Ensure text is under 280 characters
            if len(text) > 280:
                print(f"⚠️  Tweet too long ({len(text)} chars), truncating...")
                text = text[:277] + "..."
            
            # Post tweet using v2 API
            response = self.client.create_tweet(text=text)
            
            if response.data:
                tweet_id = response.data['id']
                # Construct URL to tweet
                # Note: You'll need to replace 'YourUsername' with actual username
                tweet_url = f"https://x.com/DevUnfiltered/status/{tweet_id}"
                return tweet_url
            else:
                print("❌ Tweet posting failed - no response data")
                return None
                
        except tweepy.TweepyException as e:
            print(f"❌ Tweepy error: {e}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error posting tweet: {e}")
            return None
    
    def get_tech_trends(self, count=5):
        """
        Fetch trending topics relevant to tech/dev community
        
        Args:
            count (int): Number of trends to return
            
        Returns:
            list: Trending tech topics
        """
        try:
            # Try to get trending topics from X API
            # Note: Trending topics require Premium or Enterprise access
            # This is a fallback implementation that searches for popular tech topics
            
            trends = self._search_trending_tech_topics(count)
            
            if trends and len(trends) > 0:
                return trends
            else:
                # Fallback to curated trending topics
                return self._get_fallback_trends(count)
                
        except Exception as e:
            print(f"⚠️  Error fetching trends: {e}")
            return self._get_fallback_trends(count)
    
    def _search_trending_tech_topics(self, count):
        """
        Search for currently popular tech topics on X
        
        Args:
            count (int): Number of topics to find
            
        Returns:
            list: List of trending topics
        """
        try:
            # Keywords to search for trending tech discussions
            tech_keywords = [
                'TypeScript', 'JavaScript', 'Python', 'React', 'Vue',
                'AI coding', 'Copilot', 'Cursor', 'ChatGPT',
                'Next.js', 'Remix', 'Svelte', 'Solid',
                'DevOps', 'Kubernetes', 'Docker',
                'Web3', 'Rust', 'Go', 'Zig',
                'Remote work', 'Developer productivity',
                'TDD', 'Clean code', 'Code review',
                'Bootcamp', 'CS degree', 'Self-taught developer'
            ]
            
            # Search for recent tweets with these keywords
            # Note: This requires elevated access to X API
            trending = []
            
            for keyword in random.sample(tech_keywords, min(count * 2, len(tech_keywords))):
                try:
                    # Search recent tweets
                    response = self.client.search_recent_tweets(
                        query=f"{keyword} -is:retweet lang:en",
                        max_results=10,
                        tweet_fields=['public_metrics']
                    )
                    
                    if response.data:
                        # Check engagement to determine if trending
                        total_engagement = sum(
                            tweet.public_metrics['like_count'] + 
                            tweet.public_metrics['retweet_count']
                            for tweet in response.data
                        )
                        
                        # If high engagement, consider it trending
                        if total_engagement > 100:
                            trending.append(keyword)
                            
                            if len(trending) >= count:
                                break
                                
                except tweepy.TweepyException:
                    # Continue if search fails for this keyword
                    continue
            
            return trending[:count] if trending else None
            
        except Exception as e:
            print(f"⚠️  Search trending failed: {e}")
            return None
    
    def _get_fallback_trends(self, count):
        """
        Get fallback trending topics when API access is limited
        Uses a curated list of current tech debates and hot topics
        
        Args:
            count (int): Number of topics to return
            
        Returns:
            list: Curated trending topics
        """
        # Updated for January 2026 - these are evergreen debate topics
        # that consistently drive engagement in dev community
        
        evergreen_hot_topics = [
            # Language wars
            "TypeScript vs JavaScript",
            "Python vs Go debate",
            "Rust hype cycle",
            
            # Framework battles
            "React vs Vue 2026",
            "Next.js vs Remix",
            "Angular still relevant?",
            
            # AI coding tools
            "Cursor vs Copilot",
            "ChatGPT for coding",
            "AI replacing junior devs",
            "Claude vs ChatGPT for code",
            
            # Development practices
            "TDD worth it?",
            "Pair programming effectiveness",
            "Code review best practices",
            "Clean code principles",
            
            # Career topics
            "Bootcamp vs CS degree 2026",
            "Remote work culture",
            "Job hopping strategy",
            "Developer burnout",
            "Imposter syndrome",
            
            # Architecture debates
            "Microservices vs monolith",
            "Serverless worth it?",
            "GraphQL vs REST",
            "NoSQL vs SQL",
            
            # Tooling debates
            "VS Code vs Neovim",
            "Git workflow strategies",
            "Docker in development",
            "CI/CD best practices",
            
            # Web3 and emerging tech
            "Web3 still a thing?",
            "Blockchain for developers",
            "AI agents coding",
            "Quantum computing timeline",
            
            # Productivity and culture
            "4-day work week",
            "Developer productivity metrics",
            "Meeting culture killing dev time",
            "Documentation vs code quality",
            "Tech debt management",
            
            # Industry topics
            "Tech layoffs 2026",
            "Salary transparency",
            "Big Tech vs startups",
            "Open source sustainability",
        ]
        
        # Shuffle and return requested count
        random.shuffle(evergreen_hot_topics)
        return evergreen_hot_topics[:count]
    
    def get_account_info(self):
        """
        Get authenticated user's account information
        
        Returns:
            dict: Account information
        """
        try:
            user = self.client.get_me()
            if user.data:
                return {
                    'id': user.data.id,
                    'name': user.data.name,
                    'username': user.data.username
                }
            return None
        except Exception as e:
            print(f"❌ Error fetching account info: {e}")
            return None
    
    def verify_credentials(self):
        """
        Verify that API credentials are working
        
        Returns:
            bool: True if credentials valid
        """
        try:
            user = self.get_account_info()
            if user:
                print(f"✅ Authenticated as: @{user['username']}")
                return True
            else:
                print("❌ Authentication failed")
                return False
        except Exception as e:
            print(f"❌ Credential verification error: {e}")
            return False


# Testing
if __name__ == "__main__":
    print("Testing X Handler...\n")
    
    handler = XHandler()
    
    # Test credential verification
    print("\n1. Testing credential verification:")
    if handler.verify_credentials():
        print("✅ Credentials verified")
    else:
        print("❌ Credentials invalid")
    
    # Test trend fetching
    print("\n2. Testing trend fetching:")
    trends = handler.get_tech_trends(count=5)
    print(f"Trending topics: {trends}")
    
    # Test posting (commented out to avoid spam)
    # print("\n3. Testing tweet posting:")
    # test_tweet = "Test tweet from DevUnfiltered bot - ignore this! 🤖"
    # url = handler.post_tweet(test_tweet)
    # if url:
    #     print(f"✅ Tweet posted: {url}")
    # else:
    #     print("❌ Tweet posting failed")
    
    print("\n✅ All tests complete")
