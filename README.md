# ManUtdScoreBot 🟥⚽

**ManUtdScoreBot** is a Python bot that tweets whenever **Manchester United** scores a goal. It fetches live match data using [API-FOOTBALL](https://www.api-football.com/) and posts updates to your Twitter/X account.

> ⚠️ **Note:** API keys are hidden for security. This project has only been tested using `print()` statements. A paid X developer account is required for actual tweeting.

---

## Features

- Fetch upcoming Manchester United fixtures.
- Monitor live matches.
- Detect goals scored by Manchester United.
- Post goal updates to a Twitter/X account (once API access is available).

---

## Requirements

- Python 3.9+
- Tweepy (`pip install tweepy`)
- Requests (`pip install requests`)
- Access to:
  - X (Twitter) developer API keys
  - API-FOOTBALL key

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ManUtdScoreBot.git
cd ManUtdScoreBot

Step 2: Create a .env file

In the project root, create a file called .env and add your API credentials. These are hidden for security and should never be shared publicly.

consumer_key='YOUR_TWITTER_CONSUMER_KEY'
consumer_secret='YOUR_TWITTER_CONSUMER_SECRET'
access_token='YOUR_TWITTER_ACCESS_TOKEN'
access_token_secret='YOUR_TWITTER_ACCESS_TOKEN_SECRET'
API_FOOTBALL_KEY='YOUR_API_FOOTBALL_KEY'

Step 3: Install dependencies
pip install tweepy requests
