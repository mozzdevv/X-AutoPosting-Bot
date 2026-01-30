import pandas as pd
import os
import random
import time
from datetime import datetime

CSV_PATH = '/home/ubuntu/upload/sales.csv'
STATE_FILE = '/home/ubuntu/posted_deals.txt'

def get_next_deal():
    df = pd.read_csv(CSV_PATH)
    
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            posted_ids = set(f.read().splitlines())
    else:
        posted_ids = set()
    
    # Filter out already posted deals
    remaining_deals = df[~df['id'].astype(str).isin(posted_ids)]
    
    if remaining_deals.empty:
        # If all deals are posted, reset or handle accordingly
        # For now, let's just pick a random one if empty to keep the bot active
        deal = df.sample(n=1).iloc[0]
    else:
        # Pick the first one or a random one from remaining
        deal = remaining_deals.iloc[0]
        
    return deal

def format_post(deal):
    name = deal['name']
    price = deal['priceInCents'] / 100
    retail = deal['retailPriceInCents'] / 100
    discount = round((1 - price / retail) * 100) if retail > 0 else 0
    slug = deal['slug']
    
    # Affiliate link construction (assuming a base URL + slug)
    # The user mentioned affiliate links, I'll use a placeholder or the slug
    link = f"https://stacksocial.com/sales/{slug}?rid=12345" # Placeholder RID
    
    # Format: Short, punchy opener -> value/what you get -> hook question
    # We can use LLM to generate these variations later, but for now, a template
    
    opener = f"🔥 {name} lifetime deal!"
    value = f"Get this for just ${price:.2f} ({discount}% off retail of ${retail:.2f})."
    hook = "Ready to level up your workflow?"
    
    post_text = f"{opener}\n\n{value}\n\n{hook}\n\n{link}"
    return post_text, str(deal['id'])

def mark_as_posted(deal_id):
    with open(STATE_FILE, 'a') as f:
        f.write(f"{deal_id}\n")

if __name__ == "__main__":
    deal = get_next_deal()
    post_content, deal_id = format_post(deal)
    print(f"POST_CONTENT_START\n{post_content}\nPOST_CONTENT_END")
    print(f"DEAL_ID:{deal_id}")
