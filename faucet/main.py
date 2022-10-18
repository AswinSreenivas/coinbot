"""
Check for faucet requests and send tokens.
"""
import time
import tweepy

from scrape import get_networks_and_addresses, get_mentions, TWEEPY_API
from fund import send_tokens


def run():
    """Check for faucet requests and send tokens."""
    funded = {}
    checked_mentions = set()
    while True:
        print("Checking for faucet requests...")
        yesterday_timestamp = int(time.time()) - 86400
        mentions = get_mentions(username="trbfaucet", label="faucettest", api=TWEEPY_API, from_date=yesterday_timestamp)

        new_mentions = []
        for mention in mentions:
            if isinstance(mention, tweepy.models.Status):
                if mention.id in checked_mentions:
                    continue

                # check if user funded in last 3 hours
                if mention.user.screen_name in funded and (int(time.time()) - funded[mention.user.screen_name] < 60 * 60 * 3):
                    print("Already funded this user in the last 3 hours:", mention.user.screen_name)
                    continue

                new_mentions.append(mention)
                checked_mentions.add(mention.id)

                print("From: ", mention.user.screen_name)
        
        faucet_requests = get_networks_and_addresses(new_mentions)
        print("Faucet requests:", faucet_requests)
        
        for chain_id, address in faucet_requests:
            success = send_tokens(chain_id, address)
            if success:
                print(f"Sent tokens to {address} on chain {chain_id}")
                funded[mention.user.screen_name] = time.time()

        time.sleep(60)


if __name__ == "__main__":
    run()