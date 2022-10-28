"""
Retrieve gas price source based on chain id
"""
from typing import Optional
import requests

from logging import Logger


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


async def fetch_goerli_gas_price(speed: str = "safeLow") -> Optional[int]:
        """Fetch estimated gas prices for Goerli."""
        try:
            prices = requests.get("https://www.gasnow.org/api/v3/gas/price").json()
        except requests.JSONDecodeError:
            logger.error("Error decoding JSON response from gasnow")
            return None
        except Exception as e:
            logger.error(f"Error fetching gasnow gas prices: {e}")
            return None

        if speed not in prices["data"]:
            logger.error(f"Invalid gas price speed for gasnow: {speed}")
            return None

        if prices["data"][speed] is None:
            logger.error("Unable to fetch gas price from gasnow")
            return None
        return int(prices["data"][speed] * 10 ** 9)


def fetch_gas_price(chain_id: int, speed: str = "safeLow") -> Optional[int]:
    """Fetch estimated gas prices for a given chain id."""
    if chain_id == 80001:
        return fetch_polygon_gas_price(speed)
    elif chain_id == 5:
        return fetch_goerli_gas_price(speed)
    else:
        logger.error(f"Unsupported chain id: {chain_id}")
        return None