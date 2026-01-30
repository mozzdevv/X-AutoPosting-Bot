import pandas as pd
import random
import os
import ast
import re

JOKES_FILE = os.path.join(os.path.dirname(__file__), '210jokes')
DEALS_FILE = os.path.join(os.path.dirname(__file__), 'Final Sales List.csv')

class ContentManager:
    def __init__(self):
        self.jokes = []
        self.deals = None
        self._load_jokes()
        self._load_deals()
    
    def _load_jokes(self):
        """
        Loads jokes from the '210jokes' file. 
        Since the file format is technically Python code (list assignment), 
        we'll parse it to extract the list.
        """
        if not os.path.exists(JOKES_FILE):
            print(f"Warning: Jokes file not found at {JOKES_FILE}")
            return

        try:
            with open(JOKES_FILE, 'r') as f:
                content = f.read()
                # Use regex or simple parsing if ast fails, but ast.literal_eval 
                # might be hard due to the variable assignment "humor_posts ="
                # We'll just strip the assignment part and parse the list.
                # Or create a dummy scope to exec.
                scope = {}
                exec(content, scope)
                self.jokes = scope.get('humor_posts', [])
        except Exception as e:
            print(f"Error loading jokes: {e}")
            # Fallback parsing if exec fails
            self.jokes = []

    def _load_deals(self):
        """
        Loads deals from the CSV.
        Users column L for Name, Column O for Affiliate Link.
        Pandas uses 0-based indexing: L is 11, O is 14.
        """
        if not os.path.exists(DEALS_FILE):
             # Try xlsx if csv not found
            xlsx_path = DEALS_FILE.replace('.csv', '.xlsx')
            if os.path.exists(xlsx_path):
                self.deals = pd.read_excel(xlsx_path)
            else:
                print(f"Warning: Deals file not found at {DEALS_FILE}")
                return
        else:
            self.deals = pd.read_csv(DEALS_FILE)
            
    def get_random_joke_examples(self, n=3):
        """Returns n random jokes to be used as context/style examples"""
        if not self.jokes:
            return []
        # Return a sample, or all if n > len
        return random.sample(self.jokes, min(n, len(self.jokes)))

    def get_random_deal(self):
        """
        Returns a random deal with Name and Link.
        Column L (Name) -> Index 11
        Column O (Link) -> Index 14
        """
        if self.deals is None or self.deals.empty:
            return None
        
        # Pick a random row
        row = self.deals.sample(n=1).iloc[0]
        
        # We need to handle column access carefully. 
        # If columns have headers, we should use names ideally, but user specified L and O.
        # Let's assume the file has headers and L/O are the 11th and 14th columns.
        
        try:
            # Get values by integer location
            name = row.iloc[11] 
            link = row.iloc[14]
            
            # Clean up
            if pd.isna(name) or pd.isna(link):
                return self.get_random_deal() # Retry if empty
                
            return {"name": str(name), "link": str(link)}
        except Exception as e:
            print(f"Error extracting deal: {e}")
            return None
