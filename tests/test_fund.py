from faucet.fund import get_playground_contract_info, send_tokens
import pytest


def test_get_playground_contract_info():
    """Test get_playground_contract."""
    contracts = get_playground_contract_info(80001)
    assert contracts is not None
    c = contracts[0]
    assert c.name == "tellor-playground"
    assert c.address[80001] == "0x7B8AC044ebce66aCdF14197E8De38C1Cc802dB4A"

    contracts = get_playground_contract_info(123456789)
    assert not contracts


@pytest.mark.skip(reason="Not implemented")
def test_send_tokens():
    """Test send_tokens."""
    success = send_tokens(80001, "0x123456789")
    assert success

    success = send_tokens(123456789, "0x123456789")
    assert not success

    success = send_tokens(80001, "")
    assert not success

    success = send_tokens(80001, None)
    assert not success

    success = send_tokens(None, "0x123456789")
    assert not success

    success = send_tokens(None, None)
    assert not success