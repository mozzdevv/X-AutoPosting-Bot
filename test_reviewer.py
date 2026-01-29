from agents import ReviewerAgent
from xai_wrapper import XAIClient

client = XAIClient()
reviewer = ReviewerAgent(client)

joke = "git blame\nblame the previous dev\n(me six months ago) 💀"
deal = "Tired of manual docs? PDF Reader Pro is lifetime for $39. Annotate, edit, and sign everything in seconds. Ready to save hours? https://stacksocial.com/sales/pdf-reader-pro"

print("--- Testing Joke Review ---")
s_j, r_j = reviewer.review_joke(joke)
print(f"JOKE SCORE: {s_j}, REASON: {r_j}")

print("\n--- Testing Deal Review ---")
s_d, r_d = reviewer.review_deal(deal)
print(f"DEAL SCORE: {s_d}, REASON: {r_d}")
