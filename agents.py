"""
Updated CreatorAgent and ReviewerAgent for high-engagement content strategy
Replaces joke-based generation with controversial opinions and relatable dev content
"""

import random
from xai_wrapper import XAIWrapper


class CreatorAgent:
    """
    Generates high-engagement content for X (Twitter)
    
    Content types:
    - controversial: Hot takes on dev topics that drive replies
    - relatable: Developer situation humor that gets "me too" responses
    - news_reaction: Real-time tech news commentary (optional)
    """
    
    def __init__(self, content_type='controversial'):
        """
        Initialize CreatorAgent with specified content type
        
        Args:
            content_type (str): 'controversial', 'relatable', or 'news_reaction'
        """
        self.content_type = content_type
        self.xai = XAIWrapper()
        
    def generate(self, trending_topics=None, retry_count=0, max_retries=3, self_learning_context=None):
        """
        Generate content based on content_type
        
        Args:
            trending_topics (list): Current trending topics to incorporate
            retry_count (int): Current retry attempt
            max_retries (int): Maximum retry attempts
            self_learning_context (str): Context from successful past posts
            
        Returns:
            str: Generated post content
        """
        if retry_count >= max_retries:
            return None
            
        trending_context = self._format_trending_topics(trending_topics)
        learning_note = f"\n\nPAST SUCCESS CONTEXT (What users liked before):\n{self_learning_context}" if self_learning_context else ""
        
        if self.content_type == 'controversial':
            prompt = self._get_controversial_prompt(trending_context) + learning_note
        elif self.content_type == 'relatable':
            prompt = self._get_relatable_prompt(trending_context) + learning_note
        else:  # news_reaction
            prompt = self._get_news_reaction_prompt(trending_context) + learning_note
            
        try:
            response = self.xai.generate_completion(prompt)
            return self._clean_response(response)
        except Exception as e:
            print(f"Generation error: {e}")
            return self.generate(trending_topics, retry_count + 1, max_retries, self_learning_context)

    def generate_reply(self, incoming_text, author_name):
        """
        Generate a reply to an incoming tweet
        """
        prompt = f"""You are the DevUnfiltered bot. Your persona is a senior dev who is sharp, opinionated, slightly arrogant, but highly knowledgeable. You are here to debate, roasts, or occasionally agree with logic-backed points.

INCOMING TWEET from @{author_name}:
"{incoming_text}"

TASK:
Write a reply that fits your "unfiltered" persona.
- If they agree: Double down or add a sharper point.
- If they disagree: Roast their logic (not them personally) or stand your ground firmly.
- If they are trolling: Masterfully troll them back or dismiss them with a "cope".
- STAY IN CHARACTER. Be shorter than 280 chars. 

Rules:
- NO "Change my mind" robotic endings.
- Be context-aware.
- Use casual but technical dev-speak.
- NO EM-DASHES (—).

REPLY:"""
        try:
            response = self.xai.generate_completion(prompt)
            return self._clean_response(response)
        except Exception as e:
            print(f"Reply generation error: {e}")
            return None
    
    def _format_trending_topics(self, topics):
        """Format trending topics for prompt injection"""
        if not topics or len(topics) == 0:
            return "No specific trends available - use evergreen dev topics"
        return ", ".join(topics)
    
    def _get_controversial_prompt(self, trending_context):
        """Generate prompt for controversial opinion content"""
        return f"""You are a senior developer with highly polarizing, unfiltered, and potentially unpopular opinions on software development. You are tired of the "nice" echo chamber.

Generate a SCATHINGLY CONTROVERSIAL but defensible tech opinion post for X (Twitter).

RULES:
- Start with "Unpopular opinion:", "Hot take:", "Reality check:", or "Stop doing this:"
- Be BRUTALLY HONEST. Don't sugarcoat it.
- Challenge sacred cows (Clean Code, TDD, Agile, popular frameworks).
- Provide 2-3 aggressive bullet points defending your stance.
- **CRITICAL: VARY YOUR ENDING.** Do NOT default to "Change my mind 👇". That is robotic.
- **DYNAMIC HOOKS:** contextually match the ending to the tone.
    - If Arrogant: "I said what I said.", "You know I'm right.", "Cope harder.", "Cry about it."
    - If Challenging: "Prove me wrong.", "Debate me.", "Am I wrong?", "Try to deny it."
    - If Inquisitive: "Why do you disagree?", "Who limits themselves like this?"
- **AVOID 👇 EMOJI** unless absolutely necessary. Use other emojis or none.
- Keep total length under 280 characters.
- NO NSFW, NO HATE SPEECH.
- **NO EM-DASHES (—).** Use standard hyphens (-), colons (:), or just newlines.

TOPICS TO ROAST:
- Framework cults (React bloat, Tailwind ugliness)
- "Best practices" waste (TDD, Clean Code obsessions)
- Career lies (bootcamps, "passion" exploitation)
- AI doom/hype (be realistic or scary)

CURRENT TRENDING TOPICS:
{trending_context}

GOOD EXAMPLES (Note the varied endings):
"Hot take: TypeScript is a crutch for bad mental models.

• Compile times kill flow
• JSDoc > TS definitions
• It's just Java with extra steps

Prove me wrong."

"Reality check: 'Building in public' is just procrastination.

• Revenue > Likes
• Code > Content
• Users don't care about your journey

I said what I said."

"Stop using Microservices for your MVP.

• You aren't Google
• Network latency is real
• Monoliths ship faster

Why make your life hard available?"

Generate ONE highly polarizing post now. DYNAMIC ENDING REQUIRED:"""

    def _get_relatable_prompt(self, trending_context):
        """Generate prompt for relatable developer content"""
        return f"""You are a developer who experiences the same frustrations and funny moments as everyone else in tech.

Generate a relatable developer situation post that will get "me too" responses and shares.

RULES:
- Describe a specific, common developer experience
- Use conversational, casual tone (lowercase is fine)
- Include a punchline or observation
- End with engagement hook: "Who else? 👀" or "Just me? 🤷‍♂️" or "Relatable? 💀" or "Anyone else? 😅"
- Keep under 280 characters
- **NO EM-DASHES (—).** Use standard hyphens (-).
- Avoid generic "coding is hard" - be SPECIFIC to a situation
- Use humor, irony, or self-deprecation

RELATABLE SITUATIONS:
- Time estimation failures ("should take 2 hours" → 2 days)
- Debugging mysteries (works on my machine, production breaks)
- Meeting interruptions during flow state
- Stack Overflow dependency for basic syntax
- Git commit message struggles ("fix stuff", "more fixes", "final fix I swear")
- Imposter syndrome moments
- Coffee/energy drink rituals
- Browser tab hoarding (47 tabs open, still googling same thing)
- Productivity theater (looking busy but actually stuck)
- Copy-paste from Stack Overflow shame
- "Quick fix" that breaks everything
- Monday morning code review of Friday night commits

CURRENT TRENDING TOPICS:
{trending_context}

BAD EXAMPLES (too generic):
"Coding is hard sometimes"
"Developers drink coffee"
"Bugs are annoying"

GOOD EXAMPLES:
"Me: 'I'll just add one small feature'

*3 hours later*

Me: 'Why did I refactor the entire codebase and now nothing works'

Who else? 👀"

"that moment when you fix a bug and 3 new ones appear like a hydra

just gonna pretend I didn't see them and push to prod 💀

Relatable? 😅"

"me explaining my code in the PR:
'it works trust me'

me explaining why it doesn't work in production:
*writes doctoral thesis*

Just me? 🤷‍♂️"

"opening 47 stack overflow tabs to solve one error then forgetting which tab had the solution is my core programming skill

Anyone else? 👀"

Generate ONE relatable developer post now. Make it SPECIFIC and funny:"""

    def _get_news_reaction_prompt(self, trending_context):
        """Generate prompt for tech news reaction content"""
        return f"""You are a developer who provides quick, insightful reactions to breaking tech news.

Generate a tech news reaction post that provides value and drives discussion.

RULES:
- Reference specific recent tech news or trend
- Provide 2-3 bullet points on "what this means for devs"
- End with your hot take or prediction
- Include engagement hook: "What do you think? 🤔" or "Thoughts? 👇"
- Keep under 280 characters total
- **NO EM-DASHES (—).** Use standard hyphens (-).
- Be opinionated but informed
- Focus on PRACTICAL implications for developers

FORMAT:
[Company/Tool] just [announcement]

What this means for devs:
• [Practical impact 1]
• [Practical impact 2]
• [Practical impact 3]

[Your hot take/prediction]

[Engagement hook]

CURRENT TRENDING TOPICS:
{trending_context}

EXAMPLE:
"OpenAI just dropped GPT-5 with 10x better code generation

What this means for devs:
• Junior roles getting squeezed
• Senior roles shift to AI supervision
• Prompt engineering = new core skill

This accelerates the already brutal job market. Adapt or get replaced.

What do you think? 🤔"

Generate ONE tech news reaction post now:"""

    def _clean_response(self, response):
        """Clean up AI response to extract just the post content"""
        # Remove any markdown formatting
        response = response.strip()
        
        # Remove common AI preambles
        unwanted_prefixes = [
            "Here's a post:",
            "Here is a post:",
            "Post:",
            "Tweet:",
            "Here's a controversial opinion:",
            "Here's a relatable post:",
        ]
        
        for prefix in unwanted_prefixes:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()
        
        # Remove quotes if AI wrapped response in them
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]
        
        # Ensure under 280 characters
        if len(response) > 280:
            response = response[:277] + "..."
            
        return response


class ReviewerAgent:
    """
    Evaluates generated content for engagement potential and quality
    Scores posts 0-10 based on engagement hooks, controversy, and quality
    """
    
    def __init__(self, min_score=8):
        """
        Initialize ReviewerAgent
        
        Args:
            min_score (int): Minimum score required to approve post (default 8)
        """
        self.xai = XAIWrapper()
        self.min_score = min_score
    
    def evaluate(self, post_text, content_type='controversial'):
        """
        Evaluate post for engagement potential
        
        Args:
            post_text (str): The post to evaluate
            content_type (str): Type of content being evaluated
            
        Returns:
            tuple: (score: int, feedback: str)
        """
        prompt = self._get_evaluation_prompt(post_text, content_type)
        
        try:
            response = self.xai.generate_completion(prompt)
            score, feedback = self._parse_evaluation(response)
            return score, feedback
        except Exception as e:
            print(f"Evaluation error: {e}")
            return 0, f"Evaluation failed: {str(e)}"
    
    def _get_evaluation_prompt(self, post_text, content_type):
        """Generate evaluation prompt based on content type"""
        return f"""You are an expert at evaluating X (Twitter) content for engagement potential in the developer/tech community.

Rate this post on a scale of 0-10 based on these criteria:

ENGAGEMENT POTENTIAL (50% of score):
- Does it ask a question or invite response?
- Does it have an engagement hook (emoji, "what do you think", "who else", "change my mind", etc.)?
- Will it drive replies and discussion?
- Does it make people want to quote tweet or share?

CONTROVERSY/INTEREST (30% of score):
- Is it thought-provoking or challenging conventional wisdom?
- Is it specific enough to be interesting but broad enough to be relatable?
- Does it take a clear position people can agree/disagree with?
- Will it spark debate without being toxic?

QUALITY (20% of score):
- Proper length (under 280 characters)?
- Clear and concise?
- Free of typos and grammatical errors?
- Appropriate tone for tech/dev audience?
- Professional enough while still being engaging?

POST TO EVALUATE:
"{post_text}"

CONTENT TYPE: {content_type}

STRICT REQUIREMENTS FOR 8+ SCORE:
- MUST have engagement hook (question, call to action, "who else", etc.)
- MUST be under 280 characters
- MUST be specific and defensible (not generic)
- MUST drive replies (not just likes)

Respond in EXACTLY this format:
SCORE: [0-10]
ENGAGEMENT: [0-10] - [brief reason]
CONTROVERSY: [0-10] - [brief reason]
QUALITY: [0-10] - [brief reason]
OVERALL_FEEDBACK: [1-2 sentences on strengths and how to improve if score < 8]

Be harsh. Only exceptional posts should score 8+. Most posts should be 5-7."""

    def _parse_evaluation(self, response):
        """
        Parse the evaluation response to extract score and feedback
        
        Args:
            response (str): Raw evaluation response from AI
            
        Returns:
            tuple: (score: int, feedback: str)
        """
        try:
            lines = response.strip().split('\n')
            score = 0
            feedback_parts = []
            
            for line in lines:
                line = line.strip()
                
                # Extract overall score
                if line.startswith('SCORE:'):
                    score_text = line.split(':')[1].strip()
                    # Extract just the number
                    score = int(''.join(filter(str.isdigit, score_text.split()[0])))
                
                # Collect all feedback lines
                if any(line.startswith(prefix) for prefix in ['ENGAGEMENT:', 'CONTROVERSY:', 'QUALITY:', 'OVERALL_FEEDBACK:']):
                    feedback_parts.append(line)
            
            feedback = '\n'.join(feedback_parts)
            
            # Validate score is in range
            score = max(0, min(10, score))
            
            return score, feedback
            
        except Exception as e:
            print(f"Error parsing evaluation: {e}")
            print(f"Raw response: {response}")
            return 0, f"Failed to parse evaluation: {str(e)}"
    
    def passes_threshold(self, score):
        """Check if score meets minimum threshold"""
        return score >= self.min_score
    
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
            'prove me wrong',
            'am i wrong',
            'i said what i said',
            'cope',
            'cry about it',
            'debate me',
            'agree',
            'disagree',
            'opinion',
            'wrong',
            'right',
            'deny it',
            'why',
        ]
        
        text_lower = text.lower()
        return any(hook in text_lower for hook in hooks)


# Example usage and testing
if __name__ == "__main__":
    print("Testing CreatorAgent and ReviewerAgent...\n")
    
    # Test controversial content
    print("=== CONTROVERSIAL CONTENT TEST ===")
    creator = CreatorAgent(content_type='controversial')
    trending = ['TypeScript', 'AI coding tools', 'Remote work']
    
    for i in range(3):
        print(f"\nPost {i+1}:")
        post = creator.generate(trending_topics=trending)
        print(f"Content: {post}")
        print(f"Length: {len(post)} chars")
        
        reviewer = ReviewerAgent()
        score, feedback = reviewer.evaluate(post, content_type='controversial')
        print(f"\nScore: {score}/10")
        print(f"Feedback:\n{feedback}")
        print(f"Has engagement hook: {reviewer.has_engagement_hook(post)}")
        print(f"Passes threshold: {reviewer.passes_threshold(score)}")
        print("-" * 80)
    
    # Test relatable content
    print("\n\n=== RELATABLE CONTENT TEST ===")
    creator_relatable = CreatorAgent(content_type='relatable')
    
    for i in range(3):
        print(f"\nPost {i+1}:")
        post = creator_relatable.generate(trending_topics=trending)
        print(f"Content: {post}")
        print(f"Length: {len(post)} chars")
        
        reviewer = ReviewerAgent()
        score, feedback = reviewer.evaluate(post, content_type='relatable')
        print(f"\nScore: {score}/10")
        print(f"Feedback:\n{feedback}")
        print(f"Has engagement hook: {reviewer.has_engagement_hook(post)}")
        print(f"Passes threshold: {reviewer.passes_threshold(score)}")
        print("-" * 80)
