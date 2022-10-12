"""Scrape mentions of @trbfaucet from Twitter.

Filter invalid mentions, send test tokens to valid mentions"""

import tweepy
import time
import os

auth = tweepy.OAuth1UserHandler(
    consumer_key = os.getenv('TWITTER_CONSUMER_KEY'),
    consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET'),
    access_token = os.getenv('TWITTER_ACCESS_TOKEN'),
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

api = tweepy.API(auth)

faucet_user = api.get_user('trbfaucet')

yesterday_timestamp = int(time.time()) - 86400
# get mentions since yesterday
mentions = api.mentions_timeline(since_id=yesterday_timestamp)

# filter out invalid mentions
valid_mentions = []
for mention in mentions:
    pass
