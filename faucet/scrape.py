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

def get_mentions(label: str, from_date: int, api: tweepy.API, username: str) -> list:
    """Get mentions of a user since a given date."""
    # convert from_date timestamp to format required by Twitter API 'yyyyMMddHHmm'
    from_date = time.strftime('%Y%m%d%H%M', time.gmtime(from_date))
    query = f"to:{username}"
    mentions = api.search_30_day(label=label, query=query, fromDate=from_date)
    return mentions

yesterday_timestamp = int(time.time()) - 86400
mentions = get_mentions(username="trbfaucet", label="faucettest", api=api, from_date=yesterday_timestamp)
for mention in mentions:
    if isinstance(mention, tweepy.models.Status):
        print("From: ", mention.user.screen_name)
        print(mention.text)


# filter out previous mentions using tweet id


def get_networks_and_addresses(mentions: list) -> dict:
    """Get networks and addresses from mentions."""
    pass
