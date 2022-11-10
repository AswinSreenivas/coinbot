"""
Retrieve gas price source based on chain id
"""
from typing import Callable, Optional
import requests
from telliot_core.gas.legacy_gas import ethgasstation

from logging import Logger

from faucet.constants import SUPPORTED_CHAINS


logger = Logger(__name__)


async def fetch_polygon_gas_price(speed: str = "safeLow") -> Optional[int]:
    """Fetch estimated gas prices for Polygon mainnet."""
    try:
        prices = requests.get("https://gasstation-mainnet.matic.network").json()
    except requests.JSONDecodeError:
        logger.error("Error decoding JSON response from matic gas station")
        return None
    except Exception as e:
        logger.error(f"Error fetching matic gas prices: {e}")
        return None

    if speed not in prices:
        logger.error(f"Invalid gas price speed for matic gasstation: {speed}")
        return None

    if prices[speed] is None:
        logger.error("Unable to fetch gas price from matic gasstation")
        return None
    return int(prices[speed])


async def fetch_goerli_gas_price(speed: str = "average") -> Optional[int]:
    """Fetch estimated gas prices for Goerli."""
    return await ethgasstation(speed)


async def fetch_gas_price(chain_id: int) -> Optional[int]:
    """Fetch estimated gas prices for a given chain id."""
    if chain_id == 80001:
        return await fetch_polygon_gas_price()
    elif chain_id == 5:
        return await fetch_goerli_gas_price()
    else:
        raise ValueError(f"Unsupported chain id: {chain_id}")


def get_native_token_symbol(chain_id: int) -> str:
    """Get native token symbol for given chain id."""
    if chain_id in SUPPORTED_CHAINS:
        return SUPPORTED_CHAINS[chain_id]["native_token_symbol"]
    else:
        raise ValueError(f"Unsupported chain id: {chain_id}")


async def check_available_funds(account: str, chain_id: int, log: Callable, alert: Callable) -> bool:
    """
    Check if funding acount has enough testnet Goerli TRB, ETH (Goerli), & testnet MATIC.

    Returns True if account has enough funds to cover gas price times
    the estimated gas for a transfer transaction. Otherwise, returns False.
    """
    enough_native_token = check_native_token_funds(account=account, chain_id=chain_id)

    if not enough_native_token:
        symbol = get_native_token_symbol(chain_id=chain_id)
        msg = f"Funding account {account} has insufficient {symbol}"
        log(msg)
        alert(msg)
        return False
    
    if chain_id in NO_FAUCET_TRB:
        enough_trb = check_trb_funds(account=account, chain_id=chain_id)
        if not enough_trb:
            msg = f"Funding account {account} has insufficient TRB"
            log(msg)
            alert(msg)
            return False
    
    return True
