
import tweepy # Import Twitter API library
import os # For hidden API keys
import requests 
import time 

def load_env_file(filepath):
    with open(filepath) as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key.strip()] = value.strip().strip("'").strip('"')

load_env_file('.env')

consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)

# Verify authentication
user = api.verify_credentials()
print(user.name)

# Real API hidden for security
API_FOOTBALL_KEY = os.getenv('API_FOOTBALL_KEY')

TEAM_ID = 33  # Manchester United's team ID in api-sports.io

# Keep track of tweeted goals
tweeted_goal_ids = set()

# 
# 1: Fetch upcoming fixtures
def get_upcoming_fixtures():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    params = {"team": TEAM_ID, "status": "NS"}  # NS = Not Started
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return [match["fixture"]["id"] for match in data["response"]]


# 2: Get live match status
def get_live_fixtures():
    url = "https://v3.football.api-sports.io/fixtures"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    params = {"team": TEAM_ID, "status": "LIVE"}  # Only live matches
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return [match["fixture"]["id"] for match in data["response"]]


# 3: Get goals for a fixture
def get_goals_for_fixture(fixture_id):
    url = f"https://v3.football.api-sports.io/fixtures/events?fixture={fixture_id}"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    goals = []
    if data["response"]:
        for event in data["response"]:
            if event["type"] == "Goal" and event["team"]["id"] == TEAM_ID:
                scorer = event["player"]["name"]
                minute = event["time"]["elapsed"]
                # Unique ID to prevent duplicate tweets
                goal_id = f"{fixture_id}-{minute}-{scorer}"
                goals.append({"id": goal_id, "scorer": scorer, "minute": minute})
    return goals

# 4: Get live score for a fixture
def get_live_score(fixture_id):
    url = f"https://v3.football.api-sports.io/fixtures?id={fixture_id}"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    if data["response"]:
        goals = data["response"][0]["goals"]
        return f"{goals['home']} - {goals['away']}"
    return "Score unavailable"

# -----------------------------
# Main loop
# -----------------------------
# 1: fetch upcoming fixtures
future_fixtures = get_upcoming_fixtures()
print(f"Upcoming fixtures: {future_fixtures}")

while True:
    # 2: check which fixtures are live
    live_fixtures = get_live_fixtures()
    
    for fixture_id in live_fixtures:
        # 3: get goals
        goals = get_goals_for_fixture(fixture_id)
        score = get_live_score(fixture_id)
        
        for goal in goals:
            if goal["id"] not in tweeted_goal_ids:
                tweet = f"⚽ Goal! {goal['scorer']} scores for Manchester United at {goal['minute']}'\nCurrent score: {score}"
                api.update_status(tweet)
                tweeted_goal_ids.add(goal["id"])
    
    #Check every minute 
    time.sleep(60)

    