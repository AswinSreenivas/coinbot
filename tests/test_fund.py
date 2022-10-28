from faucet.fund import get_playground_contract_info, send_tokens, get_rpc_endpoint, get_playground_contract
import pytest


def test_get_playground_contract_info():
    """Test get_playground_contract."""
    c = get_playground_contract_info(80001)
    assert c is not None
    assert c.name == "tellor-playground"
    assert c.address[80001] == "0x7B8AC044ebce66aCdF14197E8De38C1Cc802dB4A"

    contracts = get_playground_contract_info(123456789)
    assert contracts is None


def test_get_rpc_endpoint():
    """Test get_rpc_endpoint."""
    endpoint = get_rpc_endpoint(80001)
    assert endpoint is not None
    assert endpoint.chain_id == 80001
    assert "https://" in endpoint.url


def test_get_playground_contract():
    """Test get_playground_contract."""
    contract_info = get_playground_contract_info(80001)
    endpoint = get_rpc_endpoint(80001)
    contract = get_playground_contract(80001, contract_info, endpoint)
    assert contract is not None
    assert contract.address == "0x7B8AC044ebce66aCdF14197E8De38C1Cc802dB4A"
    assert contract.node.chain_id == 80001
    assert "https://" in contract.node.url


@pytest.mark.skip("blah")
@pytest.mark.asyncio
async def test_send_tokens(caplog):
    """Test send_tokens."""
    # Test sending on Mumbai
    success = await send_tokens(80001, "0x5134c5a32bf3a492A2007D55E9a98d91C1eCEb6d")
    assert success

    # Test sending on Goerli
    success = await send_tokens(123456789, "0x5134c5a32bf3a492A2007D55E9a98d91C1eCEb6d")
    assert not success
    assert "No playground contract info found for chain id: 123456789" in caplog.text
