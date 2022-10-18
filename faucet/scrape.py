"""Scrape mentions of @trbfaucet from Twitter.

Filter invalid mentions, send test tokens to valid mentions"""

import tweepy
import time
import os
from dotenv import load_dotenv
import sys
from typing import Optional
from eth_utils import is_address
from constants import SUPPORTED_CHAINS

load_dotenv()

auth = tweepy.OAuthHandler(
    consumer_key = os.getenv('TWITTER_API_KEY'),
    consumer_secret = os.getenv('TWITTER_API_SECRET'),
)
auth.set_access_token(
    os.getenv('TWITTER_ACCESS_TOKEN'),
    os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

TWEEPY_API = tweepy.API(auth)

try:
    TWEEPY_API.verify_credentials()
    print("Authentication OK")
except Exception as e:
    print(f"Error during authentication: {e}")
    sys.exit(1)


def get_mentions(label: str, from_date: int, api: tweepy.API, username: str) -> list:
    """Get mentions of a user since a given date."""
    # convert from_date timestamp to format required by Twitter API 'yyyyMMddHHmm'
    from_date = time.strftime('%Y%m%d%H%M', time.gmtime(from_date))
    query = f"@{username}"
    mentions = api.search_30_day(label=label, query=query, fromDate=from_date)
    return mentions


def parse_mention_text(text: str) -> Optional[tuple]:
    """Parse mention text to get chain id and address."""
    print("Parsing mention text...")
    chain_id = None
    address = None
    for word in text.split():
        if is_address(word):
            address = word
            continue
        if word.isdigit():
            chain_id = int(word) if int(word) in SUPPORTED_CHAINS else None

    return chain_id, address if chain_id and address else None


def get_networks_and_addresses(mentions: list) -> list:
    """Get networks and addresses from mentions."""
    networks_and_addresses = []
    for mention in mentions:
        parsed = parse_mention_text(mention.text)
        if parsed is not None and None not in parsed:
            networks_and_addresses.append(parsed)
    
    return networks_and_addresses
