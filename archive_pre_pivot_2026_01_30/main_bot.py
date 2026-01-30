import os
import random
import time
import json
from datetime import datetime
from dotenv import load_dotenv

from content_manager import ContentManager
from xai_wrapper import XAIClient
from x_handler import XHandler
from agents import CreatorAgent, ReviewerAgent

# Load Env
load_dotenv()

# Configuration
LOG_FILE = "bot_activity.json"
HISTORY_FILE = "posted_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def log_activity(entry):
    """Logs activity to a JSON file for the dashboard"""
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    # Add timestamp
    entry['timestamp'] = datetime.now().isoformat()
    logs.insert(0, entry) # Prepend for latest first
    
    # Keep last 100 logs
    logs = logs[:100]
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=2)

def main():
    print("🚀 X AutoBot Continuous Mode Started!")
    
    # Initialize Components
    content_manager = ContentManager()
    xai_client = XAIClient()
    x_handler = XHandler()
    
    creator = CreatorAgent(xai_client, content_manager)
    reviewer = ReviewerAgent(xai_client)
    
    while True:
        print(f"\n--- New Cycle Started at {datetime.now().strftime('%H:%M:%S')} ---")
        
        # Decision: Joke (90%) or Deal (10%)
        is_deal = random.random() < 0.1
        post_type = "DEAL" if is_deal else "JOKE"
        
        print(f"Goal: Post a {post_type}")
        
        # Attempt Loop (Max 3 retries)
        max_retries = 3
        final_post = None
        
        for attempt in range(max_retries):
            log_entry = {"type": post_type, "attempt": attempt+1, "status": "processing"}
            
            # 1. Generate
            print(f"Generating content (Attempt {attempt+1})...")
            if is_deal:
                content = creator.generate_deal_post()
            else:
                # Sense viral trends on every joke cycle to stay fresh
                viral_trends = x_handler.search_dev_jokes()
                content = creator.generate_joke(viral_context=viral_trends)
                
            if not content:
                print("Generation failed.")
                log_entry["status"] = "generation_failed"
                log_activity(log_entry)
                continue
                
            # 2. Review
            print(f"Reviewing: {content[:50].replace('\n', ' ')}...")
            if is_deal:
                score, reason = reviewer.review_deal(content)
            else:
                score, reason = reviewer.review_joke(content)
            print(f"Score: {score}/10 - {reason}")
            
            log_entry["content"] = content
            log_entry["score"] = score
            log_entry["reason"] = reason
            
            if score >= 8:
                print("APPROVED!")
                final_post = content
                log_entry["status"] = "approved"
                log_activity(log_entry)
                break
            else:
                print("REJECTED. Retrying...")
                log_entry["status"] = "rejected"
                log_activity(log_entry)
                time.sleep(5) # Brief pause before retry
        
        # 3. Post to X
        if final_post:
            print("Posting to X...")
            result = x_handler.post_tweet(final_post)
            
            if result['status'] == 'success':
                print("Successfully Posted!")
                # Update History
                history = load_history()
                history.append({"content": final_post, "timestamp": datetime.now().isoformat(), "type": post_type})
                save_history(history)
                
                # Final Log
                log_activity({"type": post_type, "status": "posted", "content": final_post, "x_response": str(result['data'])})
            else:
                print(f"X Post Failed: {result['message']}")
                log_activity({"type": post_type, "status": "posting_error", "error": result['message'], "content": final_post})
        else:
            print("Failed to generate an approved post after max retries.")

        # --- RANDOMIZED SLEEP ---
        # Min: 25 minutes (1500 sec)
        # Max: 2 hours (7200 sec)
        sleep_seconds = random.randint(1500, 7200)
        next_run = datetime.now() + timedelta(seconds=sleep_seconds)
        
        print(f"Sleeping for {sleep_seconds // 60} minutes...")
        print(f"Next post will be attempted at: {next_run.strftime('%H:%M:%S')}")
        
        # Store state for dashboard
        with open("scheduler_state.json", "w") as f:
            json.dump({"next_run": next_run.isoformat(), "last_run": datetime.now().isoformat()}, f)
            
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    from datetime import timedelta
    main()
