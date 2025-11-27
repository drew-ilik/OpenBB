"""IBKR Provider Helpers"""
import logging
import math
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

def fetch_and_cache(self, symbol):
    if symbol in self.cache:
        return self.cache[symbol]
    data = self.connection.ib.reqMktData(symbol)
    self.cache[symbol] = data
    return data

def is_live_account(account_mode: str) -> bool:
    """Check if the current account mode is live or paper."""
    return account_mode == "live"

def normalize_result_data(raw: dict[str, Any]) -> dict[str, list[Any]]:
    """Normalize raw ticker data for use in OpenBB fetchers."""

    def process_value(v: Any) -> Any:
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    return {
        k: (
            v if isinstance(v, list)
            else [process_value(v)] if v is not None
            else []
        )
        for k, v in raw.items()
    }

def safe_getattr(obj: Any, attr: str, default: Any | None) -> Any:
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default
