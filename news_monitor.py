import requests
import heapq
from datetime import datetime, timedelta

class NewsMonitor:
    """
    Monitors real-time tech news sources:
    1. Hacker News (Top Stories)
    2. GitHub Trending (via Search API)
    """
    
    def __init__(self):
        self.hn_api_url = "https://hacker-news.firebaseio.com/v0"
    
    def get_top_tech_news(self, limit=5):
        """
        Aggregate top news from all sources
        """
        hn_news = self.get_hackernews_top(limit=3)
        gh_trends = self.get_github_trending(limit=3)
        
        # Combine and shuffle slightly or just list them
        return hn_news + gh_trends
        
    def get_hackernews_top(self, limit=5):
        """
        Fetch top stories from Hacker News
        """
        try:
            # Get top story IDs
            resp = requests.get(f"{self.hn_api_url}/topstories.json")
            if resp.status_code != 200:
                print(f"⚠️ HN API Error: {resp.status_code}")
                return []
                
            top_ids = resp.json()[:10] # Get top 10 to filter
            
            stories = []
            for item_id in top_ids:
                if len(stories) >= limit:
                    break
                    
                item_resp = requests.get(f"{self.hn_api_url}/item/{item_id}.json")
                if item_resp.status_code == 200:
                    item = item_resp.json()
                    # Filter for relevance if possible, but HN Top is usually relevant
                    title = item.get('title', '')
                    url = item.get('url', '')
                    
                    if title:
                        stories.append(f"Hacker News: {title} ({url})")
                        
            return stories
            
        except Exception as e:
            print(f"❌ Error fetching HN: {e}")
            return []

    def get_github_trending(self, limit=5):
        """
        Fetch trending repositories from GitHub
        Using the search API as a proxy for 'trending'
        """
        try:
            # Search for repos created in the last 7 days with high stars
            date_7_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            query = f"created:>{date_7_days_ago}"
            
            url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc"
            
            resp = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json'})
            
            if resp.status_code != 200:
                print(f"⚠️ GitHub API Error: {resp.status_code}")
                return []
                
            items = resp.json().get('items', [])
            trends = []
            
            for item in items[:limit]:
                name = item.get('full_name', '')
                desc = item.get('description', 'No description')
                stars = item.get('stargazers_count', 0)
                lang = item.get('language', 'Unknown')
                
                if name:
                    trends.append(f"GitHub Trend: {name} ({lang}, {stars} stars) - {desc}")
                    
            return trends
            
        except Exception as e:
            print(f"❌ Error fetching GitHub: {e}")
            return []

if __name__ == "__main__":
    monitor = NewsMonitor()
    print("Fetching News...")
    news = monitor.get_top_tech_news()
    for n in news:
        print(f"- {n}")
