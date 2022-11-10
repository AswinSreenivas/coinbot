"""
Retrieve gas price source based on chain id
"""
import os
from typing import Optional
import requests
from telliot_core.gas.legacy_gas import ethgasstation
from web3 import Web3
from telliot_core.directory import contract_directory
from telliot_core.directory import ContractInfo
from telliot_core.contract.contract import Contract
from telliot_core.model.endpoints import RPCEndpoint
from chained_accounts import ChainedAccount

from logging import Logger

from faucet.constants import SUPPORTED_CHAINS
from faucet.fund import get_rpc_endpoint


logger = Logger(__name__)


ENDPOINT_MUMBAI = get_rpc_endpoint(80001)
ENDPOINT_GOERLI = get_rpc_endpoint(5)


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


def get_contract_info(chain_id: int) -> Optional[ContractInfo]:
    """Get TRB token contract or playground contract info based on chain id."""
    if chain_id == 80001:
        contract_info = contract_directory.find(name="playground", chain_id=chain_id)
    elif chain_id == 5:
        contract_info = contract_directory.find(name="trb-token", chain_id=chain_id)
    else:
        raise ValueError(f"Unsupported chain id: {chain_id}")
    return contract_info[0] if contract_info else None


def get_rpc_endpoint(chain_id: int) -> Optional[RPCEndpoint]:
    """Get RPC endpoint for given chain id."""
    if chain_id == 80001:
        url = os.getenv("MUMBAI_NODE_URL")
    elif chain_id == 5:
        url = os.getenv("GOERLI_NODE_URL")
    else:
        return None

    endpoint = RPCEndpoint(
        chain_id = chain_id,
        url = url,
    )
    return endpoint


def get_contract(chain_id: int, contract_info: ContractInfo, node: RPCEndpoint, account: ChainedAccount) -> Contract:
    """Get playground contract instance for given chain id."""
    c = Contract(
        address = contract_info.address[chain_id],
        abi = contract_info.get_abi(),
        node = node,
        account=account,
    )
    return c
