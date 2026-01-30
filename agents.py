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
        
    def generate(self, trending_topics=None, retry_count=0, max_retries=3):
        """
        Generate content based on content_type
        
        Args:
            trending_topics (list): Current trending topics to incorporate
            retry_count (int): Current retry attempt
            max_retries (int): Maximum retry attempts
            
        Returns:
            str: Generated post content
        """
        if retry_count >= max_retries:
            return None
            
        trending_context = self._format_trending_topics(trending_topics)
        
        if self.content_type == 'controversial':
            prompt = self._get_controversial_prompt(trending_context)
        elif self.content_type == 'relatable':
            prompt = self._get_relatable_prompt(trending_context)
        else:  # news_reaction
            prompt = self._get_news_reaction_prompt(trending_context)
            
        try:
            response = self.xai.generate_completion(prompt)
            return self._clean_response(response)
        except Exception as e:
            print(f"Generation error: {e}")
            return self.generate(trending_topics, retry_count + 1, max_retries)
    
    def _format_trending_topics(self, topics):
        """Format trending topics for prompt injection"""
        if not topics or len(topics) == 0:
            return "No specific trends available - use evergreen dev topics"
        return ", ".join(topics)
    
    def _get_controversial_prompt(self, trending_context):
        """Generate prompt for controversial opinion content"""
        return f"""You are a senior developer with strong, data-backed opinions on software development practices.

Generate a controversial but defensible tech opinion post for X (Twitter) that will drive replies and engagement.

RULES:
- Start with "Unpopular opinion:" or "Hot take:" or "Controversial:" or "Real talk:"
- Make a specific claim that challenges conventional wisdom
- Provide 2-3 bullet points supporting your position
- End with "What do you think? 🤔" or "Change my mind 👇" or "Fight me 🔥" or "Thoughts? 👀"
- Keep total length under 280 characters
- Use casual, conversational tone
- Avoid generic takes - be SPECIFIC and data-driven
- Must be defensible with real reasoning

TOPICS TO CHOOSE FROM:
- Framework debates (React vs Vue, TypeScript vs JavaScript, Next.js vs Remix)
- Development practices (TDD, pair programming, code reviews, documentation)
- Career advice (bootcamps vs degrees, job hopping, remote work, salary negotiation)
- Tools and workflows (IDE choices, Git workflows, CI/CD, monorepo vs polyrepo)
- AI coding assistants (Copilot, Cursor, ChatGPT, Claude)
- Architecture decisions (microservices, monoliths, serverless)
- Programming languages (Python vs Go, Rust hype, JavaScript fatigue)

CURRENT TRENDING TOPICS:
{trending_context}

BAD EXAMPLES (too generic):
"Unpopular opinion: Writing tests is good"
"Hot take: You should learn to code"
"Controversial: Documentation matters"

GOOD EXAMPLES:
"Unpopular opinion: TypeScript is overkill for 90% of projects

Here's why:
• Most bugs aren't type-related
• Adds dev friction for small teams  
• Vanilla JS + good tests >>> TS + bad tests

What do you think? 🤔"

"Hot take: Bootcamps produce better junior devs than CS degrees in 2026

Why:
• Practical skills > theory
• Portfolio > GPA
• Ship code faster

Change my mind 👇"

"Real talk: Daily standups are productivity killers

• Breaks flow state
• Most updates belong in Slack
• Async >>> sync for remote teams

Thoughts? 👀"

Generate ONE controversial opinion post now. Be specific, be bold, be defensible:"""

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
