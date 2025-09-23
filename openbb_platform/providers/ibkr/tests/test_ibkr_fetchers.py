import asyncio
from types import SimpleNamespace

import pytest
from openbb_ibkr.models.options_chains import IBKROptionsChainsFetcher


class FakeUpdateEvent:
    """Mimics ib_async's .updateEvent with connect/disconnect semantics."""

    def __init__(self):
        self._listener = None

    def connect(self, listener=None, **_):
        self._listener = listener
        if callable(self._listener):
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = asyncio.get_event_loop()
            loop.call_soon(self._listener, None)

    def disconnect(self, listener=None, **_):
        self._listener = None


class FakeContract:
    def __init__(self, symbol="SPY"):
        self.symbol = symbol


class FakeTicker:
    """A minimal ticker carrying the attributes the fetcher reads."""

    def __init__(
        self,
        *,
        symbol="SPY",
        bid=1.23,
        ask=1.45,
        last=1.30,
        iv=0.123,
        call_oi=42,
        put_oi=11,
        call_vol=3,
        put_vol=1,
    ):
        self.updateEvent = FakeUpdateEvent()
        self.bid = bid
        self.ask = ask
        self.last = last
        self.impliedVolatility = iv
        self.callOpenInterest = call_oi
        self.putOpenInterest = put_oi
        self.callVolume = call_vol
        self.putVolume = put_vol
        self.contract = FakeContract(symbol=symbol)



@pytest.mark.asyncio
async def test_ibkr_options_chains_fetcher_monkeypatched(monkeypatch):
    """
    Unit test for IBKROptionsChainsFetcher.aextract_data with the socket call
    replaced by a FakeTicker.
    """
    if not hasattr(IBKROptionsChainsFetcher, "aextract_data"):
        raise AttributeError("Fetcher missing aextract_data")

    query = SimpleNamespace(
        symbol="SPY",
        lastTradeDateOrContractMonth="20250117",
        strike=590.0,
        right="C",
        exchange="SMART",
        multiplier="100",
        currency="USD",
    )

    fake_ib = SimpleNamespace(reqMktData=lambda *args, **kwargs: FakeTicker(symbol="SPY"))
    monkeypatch.setattr(
        IBKROptionsChainsFetcher,
        "ibkr_connection",
        SimpleNamespace(ib=fake_ib),
        raising=False,
    )
    monkeypatch.setattr(IBKROptionsChainsFetcher, "snapshot", True, raising=False)

    # Actual fetcher call
    result = await IBKROptionsChainsFetcher.aextract_data(query, credentials=None)

    payload = getattr(result, "result", result)
    if hasattr(payload, "model_dump"):
        data = payload.model_dump()
    elif hasattr(payload, "__dict__"):
        data = payload.__dict__
    else:
        data = dict(payload)

    assert data.get("underlying_symbol") in ("SPY", ["SPY"])
    assert data.get("contract_symbol") in ("SPY", ["SPY"])

    # Option descriptors
    assert data.get("expiration") in ("20250117", ["20250117"])
    assert data.get("strike") in (590.0, [590.0])
    assert data.get("option_type") in ("C", ["C"])

    # Market attributes (snapshot path produced values)
    for k in ("bid", "ask", "last", "open_interest", "volume"):
        v = data.get(k)
        assert v not in (None, []), f"{k} should be present"
