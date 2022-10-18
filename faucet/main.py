"""
Check for faucet requests and send tokens.
"""
import time

from faucet.scrape import get_networks_and_addresses
from faucet.fund import send_tokens


def run():
    """Check for faucet requests and send tokens."""
    while True:
        faucet_requests = get_networks_and_addresses()
        
        for chain_id, address in faucet_requests:
            success = send_tokens(chain_id, address)
            if success:
                print(f"Sent tokens to {address} on chain {chain_id}")
            else:
                print(f"Failed to send tokens to {address} on chain {chain_id}")

        time.sleep(60)


if __name__ == "__main__":
    run()