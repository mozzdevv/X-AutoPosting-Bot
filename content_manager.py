"""
Updated Content Manager for trending topics tracking
Ensures variety in posted content and manages topic freshness
"""

import json
import os
from datetime import datetime


class TrendingTopicsManager:
    """
    Manage trending topics and ensure variety in content
    Tracks recently used topics to avoid repetition
    """
    
    def __init__(self, history_file='topic_history.json', max_history=50):
        """
        Initialize TrendingTopicsManager
        
        Args:
            history_file (str): Path to topic history JSON file
            max_history (int): Maximum number of topics to track
        """
        self.history_file = history_file
        self.max_history = max_history
        self.recent_topics = []
        self.load_history()
    
    def load_history(self):
        """Load topic history from file"""
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                self.recent_topics = data.get('topics', [])
        except FileNotFoundError:
            self.recent_topics = []
            self.save_history()
    
    def save_history(self):
        """Save topic history to file"""
        data = {
            'topics': self.recent_topics,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.history_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_topic(self, topic):
        """
        Track a topic that was used in a post
        
        Args:
            topic (str): Topic to track
        """
        # Add topic with timestamp
        topic_entry = {
            'topic': topic,
            'timestamp': datetime.now().isoformat()
        }
        
        self.recent_topics.append(topic_entry)
        
        # Keep only max_history most recent topics
        if len(self.recent_topics) > self.max_history:
            self.recent_topics = self.recent_topics[-self.max_history:]
        
        self.save_history()
    
    def is_fresh_topic(self, topic):
        """
        Check if topic hasn't been used recently
        
        Args:
            topic (str): Topic to check
            
        Returns:
            bool: True if topic is fresh (not used in last 10 posts)
        """
        # Check last 10 topics
        recent_topic_names = [
            t['topic'].lower() 
            for t in self.recent_topics[-10:] 
            if 'topic' in t
        ]
        
        return topic.lower() not in recent_topic_names
    
    def get_fresh_topics(self, topic_list):
        """
        Filter list to only fresh topics
        
        Args:
            topic_list (list): List of topics to filter
            
        Returns:
            list: Topics that haven't been used recently
        """
        return [t for t in topic_list if self.is_fresh_topic(t)]
    
    def get_topic_suggestions(self):
        """
        Return evergreen dev topics that haven't been used recently
        
        Returns:
            list: Fresh evergreen topics
        """
        evergreen = [
            # Language debates
            "TypeScript vs JavaScript",
            "Python vs Go",
            "Rust programming language",
            "JavaScript fatigue",
            
            # Framework wars
            "React vs Vue",
            "Next.js vs Remix",
            "Angular 2026",
            "Svelte adoption",
            
            # Development practices
            "TDD effectiveness",
            "Code review best practices",
            "Pair programming",
            "Clean code principles",
            "Technical debt management",
            "Documentation importance",
            
            # AI and tools
            "AI coding assistants",
            "Copilot vs Cursor",
            "ChatGPT for coding",
            "AI replacing developers",
            
            # Career topics
            "Bootcamp vs CS degree",
            "Remote work productivity",
            "Developer burnout",
            "Imposter syndrome",
            "Job hopping strategy",
            "Salary negotiation",
            
            # Architecture
            "Microservices vs monolith",
            "Serverless architecture",
            "GraphQL vs REST",
            "Event-driven architecture",
            
            # Workflow and tools
            "Git workflow strategies",
            "VS Code vs Neovim",
            "Docker in development",
            "CI/CD pipelines",
            "Kubernetes worth it",
            
            # Industry trends
            "Tech layoffs impact",
            "Open source sustainability",
            "Web3 relevance",
            "Developer productivity metrics",
            "Meeting culture",
            "4-day work week",
        ]
        
        # Return only fresh topics
        fresh = [t for t in evergreen if self.is_fresh_topic(t)]
        
        # If all topics have been used, reset and return all
        if len(fresh) == 0:
            return evergreen
        
        return fresh
    
    def get_stats(self):
        """
        Get statistics about topic usage
        
        Returns:
            dict: Topic usage statistics
        """
        total_topics = len(self.recent_topics)
        
        if total_topics == 0:
            return {
                'total_topics_used': 0,
                'most_used_topics': [],
                'least_used_topics': []
            }
        
        # Count topic usage
        topic_counts = {}
        for entry in self.recent_topics:
            if 'topic' in entry:
                topic = entry['topic']
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        # Sort by usage
        sorted_topics = sorted(
            topic_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'total_topics_used': total_topics,
            'unique_topics': len(topic_counts),
            'most_used_topics': sorted_topics[:5],
            'least_used_topics': sorted_topics[-5:] if len(sorted_topics) > 5 else []
        }
    
    def clear_history(self):
        """Clear all topic history"""
        self.recent_topics = []
        self.save_history()


# Testing
if __name__ == "__main__":
    print("Testing TrendingTopicsManager...\n")
    
    manager = TrendingTopicsManager()
    
    # Test adding topics
    print("1. Adding test topics:")
    test_topics = [
        "TypeScript vs JavaScript",
        "React vs Vue",
        "AI coding tools",
        "TypeScript vs JavaScript",  # Duplicate
        "Remote work",
    ]
    
    for topic in test_topics:
        manager.add_topic(topic)
        print(f"Added: {topic}")
    
    # Test freshness checking
    print("\n2. Testing topic freshness:")
    print(f"Is 'TypeScript vs JavaScript' fresh? {manager.is_fresh_topic('TypeScript vs JavaScript')}")
    print(f"Is 'New Topic' fresh? {manager.is_fresh_topic('New Topic')}")
    
    # Test getting suggestions
    print("\n3. Getting topic suggestions:")
    suggestions = manager.get_topic_suggestions()
    print(f"Fresh suggestions (first 5): {suggestions[:5]}")
    
    # Test stats
    print("\n4. Topic usage statistics:")
    stats = manager.get_stats()
    print(f"Total topics used: {stats['total_topics_used']}")
    print(f"Unique topics: {stats['unique_topics']}")
    print(f"Most used topics: {stats['most_used_topics']}")
    
    print("\n✅ All tests complete")
