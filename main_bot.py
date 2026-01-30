"""
Updated main_bot.py - High-Engagement Content Strategy
Posts 2-3 times daily with 4-8 hour delays between posts
70% controversial opinions, 30% relatable content
"""

import os
import time
import random
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Import updated modules
from agents import CreatorAgent, ReviewerAgent
from x_handler import XHandler
from content_manager import TrendingTopicsManager

# Load environment variables
load_dotenv()

# Configuration
POST_FREQUENCY_HOURS_MIN = int(os.getenv('POST_FREQUENCY_HOURS_MIN', 4))
POST_FREQUENCY_HOURS_MAX = int(os.getenv('POST_FREQUENCY_HOURS_MAX', 8))
CONTROVERSIAL_WEIGHT = int(os.getenv('CONTROVERSIAL_WEIGHT', 70))
RELATABLE_WEIGHT = int(os.getenv('RELATABLE_WEIGHT', 30))
MIN_SCORE_THRESHOLD = int(os.getenv('MIN_SCORE_THRESHOLD', 8))
MAX_RETRIES = 3

# File paths
ACTIVITY_LOG = 'bot_activity.json'
POSTED_HISTORY = 'posted_history.json'


class EngagementBot:
    """
    Main bot orchestrator for high-engagement X posting
    """
    
    def __init__(self):
        """Initialize bot with handlers and managers"""
        self.x_handler = XHandler()
        self.trending_manager = TrendingTopicsManager()
        self.load_activity_log()
        self.load_posted_history()
        
    def load_activity_log(self):
        """Load or create activity log"""
        try:
            with open(ACTIVITY_LOG, 'r') as f:
                self.activity = json.load(f)
        except FileNotFoundError:
            self.activity = {
                'total_posts': 0,
                'successful_posts': 0,
                'failed_posts': 0,
                'total_rejections': 0,
                'last_post_time': None,
                'next_post_time': None
            }
            self.save_activity_log()
    
    def save_activity_log(self):
        """Save activity log to file"""
        with open(ACTIVITY_LOG, 'w') as f:
            json.dump(self.activity, f, indent=2)
    
    def load_posted_history(self):
        """Load or create posted history"""
        try:
            with open(POSTED_HISTORY, 'r') as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []
            self.save_posted_history()
    
    def save_posted_history(self):
        """Save posted history to file"""
        with open(POSTED_HISTORY, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def select_content_type(self):
        """
        Select content type based on weighted random selection
        
        Returns:
            str: 'controversial' or 'relatable'
        """
        return random.choices(
            ['controversial', 'relatable'],
            weights=[CONTROVERSIAL_WEIGHT, RELATABLE_WEIGHT],
            k=1
        )[0]
    
    def has_engagement_hook(self, text):
        """
        Check if post has engagement-driving elements
        
        Args:
            text (str): Post text to check
            
        Returns:
            bool: True if has engagement hook
        """
        hooks = [
            '?',  # Questions drive replies
            '👇', '👀', '🤔', '🤷‍♂️', '💀', '🔥', '😅',  # Engagement emojis
            'what do you think',
            'change my mind',
            'who else',
            'relatable',
            'just me',
            'thoughts',
            'fight me',
            'anyone else',
        ]
        
        text_lower = text.lower()
        return any(hook in text_lower for hook in hooks)
    
    def generate_and_review_post(self, content_type, trending_topics):
        """
        Generate post and review it, retry up to MAX_RETRIES times
        
        Args:
            content_type (str): Type of content to generate
            trending_topics (list): Current trending topics
            
        Returns:
            tuple: (post_text, score, feedback) or (None, 0, "Failed")
        """
        creator = CreatorAgent(content_type=content_type)
        reviewer = ReviewerAgent(min_score=MIN_SCORE_THRESHOLD)
        
        for attempt in range(MAX_RETRIES):
            print(f"\n{'='*80}")
            print(f"Attempt {attempt + 1}/{MAX_RETRIES} - Generating {content_type} post...")
            
            # Generate post
            post_text = creator.generate(trending_topics=trending_topics)
            
            if not post_text:
                print(f"Generation failed on attempt {attempt + 1}")
                continue
            
            print(f"Generated: {post_text}")
            print(f"Length: {len(post_text)} chars")
            
            # Review post
            score, feedback = reviewer.evaluate(post_text, content_type=content_type)
            
            print(f"\nReview Score: {score}/{MIN_SCORE_THRESHOLD}")
            print(f"Feedback:\n{feedback}")
            
            # Check if post passes threshold AND has engagement hook
            has_hook = self.has_engagement_hook(post_text)
            print(f"Has engagement hook: {has_hook}")
            
            if reviewer.passes_threshold(score) and has_hook:
                print(f"✅ POST APPROVED - Score: {score}, Has Hook: {has_hook}")
                return post_text, score, feedback
            else:
                print(f"❌ POST REJECTED - Score: {score}, Has Hook: {has_hook}")
                self.log_rejection(post_text, score, feedback, content_type)
        
        print(f"\n⚠️  Failed to generate acceptable post after {MAX_RETRIES} attempts")
        return None, 0, "Max retries exceeded"
    
    def log_rejection(self, post_text, score, feedback, content_type):
        """Log rejected post to activity"""
        self.activity['total_rejections'] += 1
        
        rejection_entry = {
            'timestamp': datetime.now().isoformat(),
            'content_type': content_type,
            'post_text': post_text,
            'score': score,
            'feedback': feedback
        }
        
        if 'rejections' not in self.activity:
            self.activity['rejections'] = []
        
        # Keep only last 50 rejections
        self.activity['rejections'].append(rejection_entry)
        if len(self.activity['rejections']) > 50:
            self.activity['rejections'] = self.activity['rejections'][-50:]
        
        self.save_activity_log()
    
    def log_success(self, post_text, score, feedback, content_type, post_url):
        """Log successful post to history"""
        success_entry = {
            'timestamp': datetime.now().isoformat(),
            'content_type': content_type,
            'post_text': post_text,
            'score': score,
            'feedback': feedback,
            'url': post_url
        }
        
        self.history.append(success_entry)
        self.save_posted_history()
        
        self.activity['successful_posts'] += 1
        self.activity['last_post_time'] = datetime.now().isoformat()
        self.save_activity_log()
    
    def log_failure(self, post_text, error, content_type):
        """Log failed post attempt"""
        self.activity['failed_posts'] += 1
        
        failure_entry = {
            'timestamp': datetime.now().isoformat(),
            'content_type': content_type,
            'post_text': post_text,
            'error': str(error)
        }
        
        if 'failures' not in self.activity:
            self.activity['failures'] = []
        
        # Keep only last 50 failures
        self.activity['failures'].append(failure_entry)
        if len(self.activity['failures']) > 50:
            self.activity['failures'] = self.activity['failures'][-50:]
        
        self.save_activity_log()
    
    def calculate_next_post_time(self):
        """Calculate random delay for next post (4-8 hours)"""
        delay_hours = random.uniform(POST_FREQUENCY_HOURS_MIN, POST_FREQUENCY_HOURS_MAX)
        next_post_time = datetime.now() + timedelta(hours=delay_hours)
        
        self.activity['next_post_time'] = next_post_time.isoformat()
        self.save_activity_log()
        
        return delay_hours * 3600  # Convert to seconds
    
    def run_posting_cycle(self):
        """
        Execute one posting cycle:
        1. Select content type
        2. Get trending topics
        3. Generate and review post
        4. Post if approved
        5. Log results
        """
        print(f"\n{'='*80}")
        print(f"🚀 STARTING POSTING CYCLE at {datetime.now().isoformat()}")
        print(f"{'='*80}")
        
        # Select content type (70% controversial, 30% relatable)
        content_type = self.select_content_type()
        print(f"Content type selected: {content_type}")
        
        # Get current trending topics
        print("\nFetching trending topics...")
        trending_topics = self.x_handler.get_tech_trends(count=3)
        print(f"Trending: {trending_topics}")
        
        # Check if we should use fresh topics
        fresh_topics = [t for t in trending_topics if self.trending_manager.is_fresh_topic(t)]
        if fresh_topics:
            selected_topics = fresh_topics
        else:
            # Use evergreen topics if all trends are stale
            selected_topics = self.trending_manager.get_topic_suggestions()[:3]
        
        print(f"Selected topics for generation: {selected_topics}")
        
        # Generate and review post
        post_text, score, feedback = self.generate_and_review_post(content_type, selected_topics)
        
        if post_text is None:
            print("\n❌ CYCLE FAILED - Could not generate acceptable post")
            return False
        
        # Attempt to post to X
        print(f"\n📤 Attempting to post to X...")
        try:
            post_url = self.x_handler.post_tweet(post_text)
            
            if post_url:
                print(f"\n✅ POST SUCCESSFUL!")
                print(f"URL: {post_url}")
                print(f"Content: {post_text}")
                
                # Log success
                self.log_success(post_text, score, feedback, content_type, post_url)
                
                # Track topics used
                for topic in selected_topics:
                    self.trending_manager.add_topic(topic)
                
                self.activity['total_posts'] += 1
                self.save_activity_log()
                
                return True
            else:
                print("\n❌ POST FAILED - X API returned no URL")
                self.log_failure(post_text, "No URL returned from X API", content_type)
                return False
                
        except Exception as e:
            print(f"\n❌ POST FAILED - Exception: {e}")
            self.log_failure(post_text, e, content_type)
            return False
    
    def run(self):
        """
        Main bot loop - runs indefinitely with random delays
        """
        print("🤖 DevUnfiltered Bot Starting...")
        print(f"Config: {CONTROVERSIAL_WEIGHT}% controversial, {RELATABLE_WEIGHT}% relatable")
        print(f"Posting every {POST_FREQUENCY_HOURS_MIN}-{POST_FREQUENCY_HOURS_MAX} hours")
        print(f"Minimum score threshold: {MIN_SCORE_THRESHOLD}/10")
        print("\n" + "="*80)
        
        while True:
            try:
                # Run posting cycle
                success = self.run_posting_cycle()
                
                # Calculate next post time
                delay_seconds = self.calculate_next_post_time()
                delay_hours = delay_seconds / 3600
                
                next_post_time = datetime.fromtimestamp(time.time() + delay_seconds)
                
                print(f"\n{'='*80}")
                if success:
                    print(f"✅ Cycle complete. Next post in {delay_hours:.2f} hours")
                else:
                    print(f"⚠️  Cycle failed. Retrying in {delay_hours:.2f} hours")
                print(f"Next post scheduled for: {next_post_time.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"{'='*80}\n")
                
                # Sleep until next post
                time.sleep(delay_seconds)
                
            except KeyboardInterrupt:
                print("\n\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"\n⚠️  Unexpected error in main loop: {e}")
                print("Waiting 1 hour before retry...")
                time.sleep(3600)


def main():
    """Entry point for bot"""
    bot = EngagementBot()
    bot.run()


if __name__ == "__main__":
    main()
