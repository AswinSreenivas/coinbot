"""
Send testnet tokens to address on a supported chain.
"""
from logging import Logger
from typing import Callable
from logging import Logger

from dotenv import load_dotenv

from faucet.constants import ENDPOINT_GOERLI, ENDPOINT_MUMBAI, TRB_ADDRESS, TRB_ABI, NO_FAUCET_TRB
from faucet.utils import get_contract_info, get_rpc_endpoint, get_contract, get_native_token_symbol

load_dotenv()


logger = Logger(__name__)


async def send_tokens(chain_id: int, address: str, log: Callable = logger.info) -> bool:
    """Send tokens to address on a supported chain."""
    contract_info = get_contract_info(chain_id)
    if not contract_info:
        log(f"No playground contract info found for chain id: {chain_id}")
        return False
    
    endpoint = get_rpc_endpoint(chain_id)
    if not endpoint:
        log(f"No RPC endpoint found for chain id: {chain_id}")
        return False
    
    contract = get_contract(chain_id, contract_info, endpoint)
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


async def check_native_token_funds(account: str, chain_id: int) -> bool:
    """Check if funding account has enough native token."""
    try:
        if chain_id == 80001:
            balance = await ENDPOINT_MUMBAI.eth.get_balance(account)
        elif chain_id == 5:
            balance = await ENDPOINT_GOERLI.eth.get_balance(account)
        else:
            raise ValueError(f"Unsupported chain id: {chain_id}")
    except Exception as e:
        logger.error(f"Error fetching native token balance: {e}")
        return False
    
    if balance < 1e18:
        return False
    return True


async def check_trb_funds(account: str, chain_id: int) -> bool:
    """Check if funding account has enough TRB."""
    try:
        trb_contract = ENDPOINT_GOERLI.eth.contract(address=TRB_ADDRESS, abi=TRB_ABI)
        balance = trb_contract.functions.balanceOf(account).call()
    except Exception as e:
        logger.error(f"Error fetching TRB balance: {e}")
        return False
    
    if balance < 1e18:
        return False
    return True
