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


logger = Logger(__name__)

# make Contract instance of playground contract using the given chain id and env address w/ funds on every supported chain
# get the playground address from telliot-core
# call the faucet function on the playground contract using the given address

# need function for checking if funding address has enough funds to send to given address


def get_playground_contract_info(chain_id: int) -> Optional[ContractInfo]:
    """Get playground contract instance for given chain id."""
    contract = contract_directory.find(name="tellor-playground", chain_id=chain_id)
    return contract


def get_rpc_endpoint(chain_id: int) -> Optional[RPCEndpoint]:
    """Get RPC endpoint for given chain id."""
    endpoint = RPCEndpoint(
        chain_id = chain_id,
        url = os.getenv("RPC_URL"),
    )
    return endpoint


def get_playground_contract(chain_id: int, contract_info: ContractInfo, node: RPCEndpoint) -> Contract:
    """Get playground contract instance for given chain id."""
    c = Contract(
        address = contract_info[chain_id].address,
        abi = contract_info.get_abi(),
        node = node,
    )
    return c



def send_tokens(chain_id: int, address: str, log: Callable = logger.error) -> bool:
    """Send tokens to address on a supported chain."""
    contract_info = get_playground_contract_info(chain_id)[0]
    if not contract_info:
        log(f"No playground contract info found for chain id: {chain_id}")
        return False
    
    endpoint = get_rpc_endpoint(chain_id)
    if not endpoint:
        log(f"No RPC endpoint found for chain id: {chain_id}")
        return False
    
    contract = get_playground_contract(contract_info, endpoint)
    contract.connect()
    if not contract:
        log(f"Unable to instantiate playground contract for chain id: {chain_id}")
        return False
    
    contract.mint(address)
    return True
