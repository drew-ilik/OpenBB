"""IBKR Provider Helpers"""

import os

from dotenv import load_dotenv


def load_ibkr_credentials():
    """Load IBKR credentials and account mode from the .env file."""
    load_dotenv()
    username = os.getenv("IBKR_USERNAME")
    password = os.getenv("IBKR_PASSWORD")
    account_mode = os.getenv("IBKR_ACCOUNT_MODE", "paper").lower()  # default to paper
    return username, password, account_mode


def is_live_account(account_mode: str) -> bool:
    """Check if the current account mode is live or paper."""
    return account_mode == "live"
