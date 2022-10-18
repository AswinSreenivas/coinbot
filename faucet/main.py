"""
Check for faucet requests and send tokens.
"""
import time
import tweepy

from faucet.scrape import get_networks_and_addresses, get_mentions, TWEEPY_API
from faucet.fund import send_tokens


def run():
    """Check for faucet requests and send tokens."""
    funded = set()
    while True:
        yesterday_timestamp = int(time.time()) - 86400
        mentions = get_mentions(username="trbfaucet", label="faucettest", api=TWEEPY_API, from_date=yesterday_timestamp)

        new_mentions = []
        for mention in mentions:
            if isinstance(mention, tweepy.models.Status):
                if mention.id in funded:
                    continue
                
                new_mentions.append(mention)
                funded.add(mention.id)

                print("From: ", mention.user.screen_name)
                print(mention.text)
        
        faucet_requests = get_networks_and_addresses(new_mentions)
        
        for chain_id, address in faucet_requests:
            success = send_tokens(chain_id, address)
            if success:
                print(f"Sent tokens to {address} on chain {chain_id}")
            else:
                print(f"Failed to send tokens to {address} on chain {chain_id}")

        time.sleep(60)


if __name__ == "__main__":
    run()