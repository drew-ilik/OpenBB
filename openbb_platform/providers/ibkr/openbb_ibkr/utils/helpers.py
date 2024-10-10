"""IBKR Provider Helpers"""



def is_live_account(account_mode: str) -> bool:
    """Check if the current account mode is live or paper."""
    return account_mode == "live"
