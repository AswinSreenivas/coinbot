"""
Send testnet tokens to address on a supported chain.
"""
from logging import Logger
from typing import Callable, Optional
import os
from logging import Logger

from telliot_core.directory import contract_directory
from telliot_core.directory import ContractInfo
from telliot_core.contract.contract import Contract
from telliot_core.model.endpoints import RPCEndpoint, EndpointList
from dotenv import load_dotenv

load_dotenv()


logger = Logger(__name__)


def check_available_funds() -> bool:
    """Check if funding acount has enough testnet Goerli TRB, testnet ETH (Goerli), & testnet MATIC."""
    raise NotImplementedError


def get_playground_contract_info(chain_id: int) -> Optional[ContractInfo]:
    """Get playground contract instance for given chain id."""
    contract_info = contract_directory.find(name="playground", chain_id=chain_id)
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


def get_playground_contract(chain_id: int, contract_info: ContractInfo, node: RPCEndpoint) -> Contract:
    """Get playground contract instance for given chain id."""
    c = Contract(
        address = contract_info.address[chain_id],
        abi = contract_info.get_abi(),
        node = node,
    )
    return c



async def send_tokens(chain_id: int, address: str, log: Callable = logger.info) -> bool:
    """Send tokens to address on a supported chain."""
    contract_info = get_playground_contract_info(chain_id)
    if not contract_info:
        log(f"No playground contract info found for chain id: {chain_id}")
        return False
    
    endpoint = get_rpc_endpoint(chain_id)
    if not endpoint:
        log(f"No RPC endpoint found for chain id: {chain_id}")
        return False
    
    contract = get_playground_contract(chain_id, contract_info, endpoint)
    contract.connect()
    if not contract:
        log(f"Unable to instantiate playground contract for chain id: {chain_id}")
        return False
    
    if chain_id == 80001:
        tx_receipt, status = await contract.write("faucet", address)
    elif chain_id == 5:
        tx_receipt, status = await contract.write("transfer", address, 1000000000000000000)

    if not status.ok or not tx_receipt:
        log(f"Unable to send tokens to address: {address} on chain id: {chain_id}")
        return False

    log(f"Sent tokens to address: {address} on chain id: {chain_id}")
    log(f"Transaction hash: {tx_receipt.transactionHash.hex()}")
    return True
