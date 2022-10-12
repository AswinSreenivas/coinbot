"""Scrape mentions of @trbfaucet from Twitter.

Filter invalid mentions, send test tokens to valid mentions"""

import tweepy
import time
import os
from dotenv import load_dotenv
import sys

load_dotenv()

auth = tweepy.OAuthHandler(
    consumer_key = os.getenv('TWITTER_API_KEY'),
    consumer_secret = os.getenv('TWITTER_API_SECRET'),
)
auth.set_access_token(
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print(f"Error during authentication: {e}")
    sys.exit(1)

faucet_user = api.get_user('trbfaucet')

yesterday_timestamp = int(time.time()) - 86400
# get mentions since yesterday
mentions = faucet_user.mentions_timeline(since_id=yesterday_timestamp)

# filter out invalid mentions
valid_mentions = []
for mention in mentions:
    print("Mention from @{}: {}".format(mention.user.screen_name, mention.text))
    print("__________________")
