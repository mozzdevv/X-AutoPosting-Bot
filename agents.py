import re

class CreatorAgent:
    def __init__(self, xai_client, content_manager):
        self.client = xai_client
        self.content_manager = content_manager

    def generate_joke(self, viral_context=None):
        """Generates a tech joke based on examples and viral trends."""
        examples = self.content_manager.get_random_joke_examples(3)
        formatted_examples = "\n\n".join([f"Example: {ex}" for ex in examples])
        
        viral_str = ""
        if viral_context:
            viral_str = "\n\nAND here are some current VIRAL dev jokes on X for structure/context inspiration:\n"
            viral_str += "\n".join([f"- {v}" for v in viral_context[:5]])

        system_prompt = (
            "You are a viral tech twitter influencer (like primeagen, techtle). "
            "You post short, punchy, cynical developer humor. "
            "Your posts are lowercase, minimal punctuation, and often use emojis like 💀, 😭, ☠️. "
            "No hashtags unless ironic. Under 280 chars. "
            "NEVER use em-dashes (—); use colons, semicolons, or standard hyphens instead."
        )
        user_prompt = (
            f"Here are some timeless examples of your style:\n{formatted_examples}{viral_str}\n\n"
            "Analyze the structure and context of both the timeless examples and the latest viral trends. "
            "Then, write a new, unique post that replicates this style but feels fresh and current. "
            "Just output the post content, nothing else."
        )
        
        content = self.client.generate_content(system_prompt, user_prompt)
        if content:
            content = content.replace("—", " - ") # Fallback safety
        return content

    def generate_deal_post(self):
        """
        Generates a deal post with research-based value proposition.
        Structure: Short opener -> Value/What you get -> Hook question -> Link.
        """
        deal = self.content_manager.get_random_deal()
        if not deal:
            return None
            
        system_prompt = (
            "You are an expert product reviewer and deal hunter for developers. "
            "Your goal is to highlight the actual utility and value of a tool. "
            "NEVER use em-dashes (—); use colons, semicolons, or standard hyphens instead."
        )
        user_prompt = (
            f"Research and write a high-converting tweet for this product: {deal['name']}\n"
            f"Affiliate Link: {deal['link']}\n\n"
            "REQUIREMENTS:\n"
            "1. Research the 'value proposition' (what problem does it solve for devs/entrepreneurs?).\n"
            "2. Follow this EXACT structure:\n"
            "   - Short, punchy opener (e.g. 'Stop wasting time on X', 'The ultimate stack addition')\n"
            "   - Value/What you get (Explain what it does and why it's a steal)\n"
            "   - Hook question (A natural transition to get people thinking)\n"
            "   - The product link\n"
            "3. Keep it under 280 characters.\n"
            "4. Tone: Authentic, hyped but not spammy.\n"
            "Just output the tweet text."
        )
        
        content = self.client.generate_content(system_prompt, user_prompt)
        
        # Fallback to ensure link is there and clean em-dashes
        if content:
            content = content.replace("—", " - ")
            if deal['link'] not in content:
                content += f"\n\n{deal['link']}"
            
        return content

class ReviewerAgent:
    def __init__(self, xai_client):
        self.client = xai_client

    def _parse_response(self, response):
        """Helper to parse SCORE and REASON from AI response."""
        if not response:
            return 0, "AI Review Failed"
        try:
            match = re.search(r"SCORE:\s*(\d+)", response)
            if match:
                score = int(match.group(1))
                reason = response.split("REASON:", 1)[1].strip() if "REASON:" in response else "No reason provided"
                return score, reason
        except Exception:
            pass
        return 0, f"Could not parse review response: {response}"

    def review_joke(self, content):
        """
        Reviews a tech joke for humor, relatability, and brand voice.
        """
        if not content:
            return 0, "No content generated"

        if "—" in content:
            return 0, "REJECTED: Contains restricted character (em-dash —). Use standard hyphens instead."

        system_prompt = "You are a ruthless viral editor and tech influencer."
        user_prompt = (
            f"Review this tech joke for a developer audience on X:\n\n'{content}'\n\n"
            "SCORING PARAMETERS (0-10):\n"
            "1. Relatability (4/10): Is this a common dev struggle or observation?\n"
            "2. Brand Voice (3/10): Is it lowercase, minimal punctuation, and cynical?\n"
            "3. Viral Spark (3/10): Does it have 'banger' potential?\n\n"
            "CRITICAL CONSTRAINTS:\n"
            "- Must be under 280 chars.\n"
            "- No corporate or 'cringe' humor.\n"
            "- MUST NOT contain em-dashes (—).\n\n"
            "Output strictly in this format: SCORE: [Total/10]. REASON: [Short reason]."
        )
        
        response = self.client.generate_content(system_prompt, user_prompt)
        return self._parse_response(response)

    def review_deal(self, content):
        """
        Reviews a SaaS deal for value, structure, and conversion potential.
        """
        if not content:
            return 0, "No content generated"

        if "—" in content:
            return 0, "REJECTED: Contains restricted character (em-dash —). Use standard hyphens instead."

        system_prompt = "You are a high-conversion performance marketer and SaaS researcher."
        user_prompt = (
            f"Review this SaaS deal post for a developer audience:\n\n'{content}'\n\n"
            "SCORING PARAMETERS (0-10):\n"
            "1. Value Research (4/10): Does it highlight a genuine problem/solution or productivity gain?\n"
            "2. Structure (3/10): Does it follow 'Short opener -> Value -> Hook question -> Link'?\n"
            "3. Hook Strength (3/10): Is the question/opener engaging enough to stop the scroll?\n\n"
            "CRITICAL CONSTRAINTS:\n"
            "- Character count < 280.\n"
            "- LINK MUST BE PRESENT.\n"
            "- Tone should be professional but hyped (NOT cynical).\n"
            "- MUST NOT contain em-dashes (—).\n\n"
            "Output strictly in this format: SCORE: [Total/10]. REASON: [Short reason]."
        )
        
        response = self.client.generate_content(system_prompt, user_prompt)
        return self._parse_response(response)
