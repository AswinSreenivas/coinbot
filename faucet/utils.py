"""
Retrieve gas price source based on chain id
"""
from typing import Optional
import requests
from telliot_core.gas.legacy_gas import ethgasstation

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