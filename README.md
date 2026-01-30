# 🔥 DevUnfiltered Bot - High-Engagement X (Twitter) Bot

**Unfiltered tech takes that start arguments**

An AI-powered X (Twitter) bot that generates controversial developer opinions and relatable tech humor designed to maximize engagement and build followers.

## 🎯 Strategy

**Content Mix:**
- 70% Controversial opinions (drive replies and debates)
- 30% Relatable developer situations (drive "me too" engagement)

**Posting Schedule:**
- 2-3 posts per day
- Random delays between 4-8 hours (mimics human behavior)
- All posts scored 8/10+ by AI reviewer before posting

**Algorithm Optimization (Jan 2026):**
- Every post includes engagement hooks (questions, CTAs, emojis)
- Optimized for reply generation (top engagement signal)
- Native content only (no external links)
- Trending topic integration

## 📋 Features

- **Dual-Agent Architecture**: Creator generates content, Reviewer scores quality
- **Trending Topic Integration**: Pulls current tech trends to inform content
- **Quality Control**: Only posts scoring 8/10+ with engagement hooks
- **Topic Variety Management**: Tracks recent topics to avoid repetition
- **Real-Time Dashboard**: Streamlit dashboard shows metrics and post history
- **Automatic Retry Logic**: Regenerates content up to 3x if quality too low
- **Human-Like Timing**: Random delays between posts to avoid bot detection

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- X (Twitter) Developer Account with API credentials
- xAI API key (for Grok 4.1)
- macOS/Linux (for daemon features) or Windows

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/X-AutoPosting-Bot.git
cd X-AutoPosting-Bot
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements_updated.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API credentials
```

Required credentials in `.env`:
```bash
# X API Credentials (from https://developer.twitter.com)
X_BEARER_TOKEN=your_bearer_token
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret

# xAI Grok API Key (from https://x.ai/api)
XAI_API_KEY=your_xai_key

# Bot Configuration
POST_FREQUENCY_HOURS_MIN=4
POST_FREQUENCY_HOURS_MAX=8
CONTROVERSIAL_WEIGHT=70
RELATABLE_WEIGHT=30
MIN_SCORE_THRESHOLD=8
```

### Running the Bot

**Start the bot:**
```bash
python main_bot_updated.py
```

**Run in background (macOS/Linux):**
```bash
nohup python main_bot_updated.py &
```

**View dashboard:**
```bash
streamlit run dashboard_updated.py
```
Then open http://localhost:8501 in your browser

### Testing Before Deployment

**Test content generation:**
```bash
python agents_updated.py
```
This will generate 3 controversial and 3 relatable posts with scores.

**Test X API connection:**
```bash
python x_handler_updated.py
```
Verifies credentials and tests trend fetching.

**Test topic management:**
```bash
python content_manager_updated.py
```
Tests topic tracking and suggestion system.

## 📊 Dashboard Features

The Streamlit dashboard (`dashboard_updated.py`) provides:

- **Real-time metrics**: Success rate, total posts, rejections
- **Performance charts**: Posts per day, content type distribution, score distribution
- **Post history**: View all posted content with scores and links
- **Rejection analysis**: See what content was rejected and why
- **Topic analytics**: Track most-used topics and variety

## 🏗️ Architecture

### File Structure
```
X-AutoPosting-Bot/
├── main_bot_updated.py          # Main bot orchestrator
├── agents_updated.py             # Creator & Reviewer agents
├── x_handler_updated.py          # X API wrapper
├── content_manager_updated.py    # Topic management
├── dashboard_updated.py          # Streamlit dashboard
├── xai_wrapper.py                # Grok API wrapper (from original)
├── requirements_updated.txt      # Python dependencies
├── .env                          # API credentials (not in git)
├── .env.example                  # Example environment file
├── bot_activity.json             # Bot activity log
├── posted_history.json           # Posted content history
└── topic_history.json            # Topic usage tracking
```

### How It Works

1. **Content Selection**: Bot randomly selects content type (70% controversial, 30% relatable)

2. **Trend Integration**: Fetches current tech trending topics from X API

3. **Content Generation**: CreatorAgent uses Grok 4.1 to generate post based on:
   - Content type
   - Trending topics
   - Evergreen dev topics
   - Engagement optimization rules

4. **Quality Review**: ReviewerAgent scores post 0-10 on:
   - Engagement potential (50%): Has hooks, drives replies
   - Controversy/Interest (30%): Thought-provoking, specific
   - Quality (20%): Grammar, length, tone

5. **Approval Gate**: Post must score ≥8 AND have engagement hook

6. **Posting**: If approved, posts to X via API

7. **Logging**: Records success/failure and updates metrics

8. **Sleep**: Random delay 4-8 hours, then repeat

## ⚙️ Configuration

### Posting Frequency
Adjust in `.env`:
```bash
POST_FREQUENCY_HOURS_MIN=4  # Minimum hours between posts
POST_FREQUENCY_HOURS_MAX=8  # Maximum hours between posts
```

### Content Mix
Adjust percentages in `.env` (must add to 100):
```bash
CONTROVERSIAL_WEIGHT=70  # 70% controversial
RELATABLE_WEIGHT=30      # 30% relatable
```

### Quality Threshold
Adjust minimum score required:
```bash
MIN_SCORE_THRESHOLD=8  # Only post if scored 8/10 or higher
```

## 🔧 Customization

### Adding New Content Types

Edit `agents_updated.py` to add new content type:

```python
def _get_new_type_prompt(self, trending_context):
    return """Your custom prompt here..."""
```

Then update `select_content_type()` in `main_bot_updated.py`.

### Modifying Review Criteria

Edit `_get_evaluation_prompt()` in `agents_updated.py` to change scoring weights or criteria.

### Custom Trending Topics

Edit `_get_fallback_trends()` in `x_handler_updated.py` to customize evergreen topics.

## 📈 Metrics & Analytics

The bot tracks:

- **Total posts**: All posting attempts
- **Successful posts**: Posts actually published
- **Failed posts**: Posts that failed to publish
- **Rejections**: Posts that didn't meet quality threshold
- **Content type distribution**: Controversial vs relatable ratio
- **Score distribution**: Quality scores over time
- **Topic usage**: Most/least used topics

Access via dashboard or directly in JSON files.

## 🚨 Troubleshooting

### Bot won't post
- Check X API credentials in `.env`
- Verify account has posting permissions
- Check `bot_activity.json` for error messages

### All posts get rejected
- Lower `MIN_SCORE_THRESHOLD` in `.env` to 7
- Check `bot_activity.json` rejections for feedback
- Run `python agents_updated.py` to test generation

### No trending topics
- Bot falls back to evergreen topics automatically
- Trending requires X API Premium (optional)

### Dashboard won't load
- Ensure Streamlit installed: `pip install streamlit`
- Check port 8501 isn't in use
- Try different port: `streamlit run dashboard_updated.py --server.port 8502`

## 🔐 Security Notes

- Never commit `.env` file (already in `.gitignore`)
- Rotate API keys regularly
- Don't share `bot_activity.json` publicly (contains post history)
- Use environment variables for all credentials

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📧 Support

For issues or questions:
- Open GitHub issue
- Check existing issues first
- Include error messages and logs

## 🎯 Roadmap

- [ ] Multi-account support
- [ ] Automated reply functionality
- [ ] Thread generation for long-form content
- [ ] A/B testing for content types
- [ ] Integration with analytics platforms
- [ ] Scheduled posting calendar
- [ ] Content calendar planning
- [ ] Automated engagement tracking

---

**Built with:**
- Python 3.10+
- xAI Grok 4.1
- Tweepy (X API v2)
- Streamlit
- Love for unfiltered dev takes 🔥
