import pandas as pd
import os
import random
import time
from datetime import datetime

CSV_PATH = '/home/ubuntu/upload/sales.csv'
STATE_FILE = '/home/ubuntu/posted_deals.txt'
LOG_FILE = '/home/ubuntu/post_history.log'

def get_next_deal():
    try:
        df = pd.read_csv(CSV_PATH)
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                posted_ids = set(f.read().splitlines())
        else:
            posted_ids = set()
        
        remaining_deals = df[~df['id'].astype(str).isin(posted_ids)]
        if remaining_deals.empty:
            deal = df.sample(n=1).iloc[0]
        else:
            deal = remaining_deals.iloc[0]
        return deal
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

def format_deal_post(deal):
    if deal is None: return "error fetching deal, we'll be back shortly. 🛠️", None
    name = deal['name']
    price = deal['priceInCents'] / 100
    retail = deal['retailPriceInCents'] / 100
    discount = round((1 - price / retail) * 100) if retail > 0 else 0
    slug = deal['slug']
    link = f"https://stacksocial.com/sales/{slug}?rid=12345"
    
    templates = [
        "absolute steal: {name} lifetime deal is live. 🚀\n\n${price:.2f} for life instead of ${retail:.2f} ({discount}% off).\n\nwho's grabbing this for their stack? 🛠️\n\n{link}",
        "stop paying monthly for {name}. 🛑\n\ngrab the lifetime access for ${price:.2f} ({discount}% off).\n\nwe ball. 🏀\n\n{link}",
        "massive W for the devs today: {name} is ${price:.2f} ({discount}% off). 💻🔥\n\nlifetime access. no subscriptions. \n\nready to level up? 📈\n\n{link}",
        "if you're still paying subscriptions for {name} you're doing it wrong. 💀\n\n${price:.2f} one-time payment. {discount}% off retail.\n\nget it while it's hot. ☕️\n\n{link}",
        "new deal alert: {name} lifetime access for ${price:.2f}. 🚨\n\nsave ${retail-price:.2f} today. \n\nhigh signal only. 📈\n\n{link}"
    ]
    
    template = random.choice(templates)
    post_text = template.format(name=name, price=price, retail=retail, discount=discount, link=link)
    return post_text, str(deal['id'])

def get_humor_post():
    humor_posts = [
        "junior dev: *writes 500 lines of clean, documented code*\nsenior dev: *deletes 400 lines and adds a single // TODO: fix this later*\n\nabsolute cinema. 🚬",
        "\"i'm an engineer\"\nbro you're just a wrapper for a gpt-4o prompt. 💀\n\nwho else is just vibing while the llm does the heavy lifting today? 🦾",
        "my code doesn't work: i sleep. 😴\nmy code works and i don't know why: real shit. 😳",
        "debugging is just being the detective in a crime movie where you are also the murderer. 🕵️‍♂️🔪",
        "nothing humbles you faster than a 'simple' css change breaking the entire production site. 📉💀",
        "npm install is just gambling for developers. will it work? will it break everything? nobody knows. 🎰💻",
        "\"it works on my machine\"\n\ngreat, let's ship your machine to the customer then. 🤡",
        "the best part of being a dev is that you can spend 8 hours automating a task that takes 5 minutes. 🧠✨",
        "me: *fixes one bug*\nmy code: *generates 3 new ones as a reward*\n\nwe are so back. 📈",
        "documentation is like sex. when it's good, it's very good. when it's bad, it's better than nothing. 📚😏",
        "i don't always test my code, but when i do, i do it in production. 🍺🔥",
        "git commit -m \"fixed stuff\"\ngit commit -m \"fixed stuff for real this time\"\ngit commit -m \"asdfghjkl\"\n\naverage dev workflow. 📉"
    ]
    return random.choice(humor_posts)

def mark_as_posted(deal_id):
    if deal_id:
        with open(STATE_FILE, 'a') as f:
            f.write(f"{deal_id}\n")

def log_post(content, type):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now()} | {type} | {content[:50]}...\n")

if __name__ == "__main__":
    # 50/50 split for full randomization between deals and humor
    if random.choice([True, False]):
        deal = get_next_deal()
        post_content, deal_id = format_deal_post(deal)
        mark_as_posted(deal_id)
        log_post(post_content, "DEAL")
    else:
        post_content = get_humor_post()
        log_post(post_content, "HUMOR")
    
    print(f"POST_CONTENT_START\n{post_content}\nPOST_CONTENT_END")
