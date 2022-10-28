from faucet.utils import fetch_gas_price
import asyncio
import pytest


@pytest.mark.asyncio
async def test_fetch_gas_price(caplog):
    gp = await fetch_gas_price(80001)
    assert gp is not None
    assert isinstance(gp, int)
    assert gp > 0

    gp = await fetch_gas_price(5)
    assert gp is not None
    assert isinstance(gp, int)
    assert gp > 0

    with pytest.raises(ValueError):
        await fetch_gas_price(123456789)
        assert "Unsupported chain id: 123456789" in caplog.text
