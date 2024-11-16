"""IBKR Options Chains Model."""

# pylint: disable=unused-argument
import os
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional
from warnings import warn

from dotenv import load_dotenv
from ib_async.contract import Option
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.options_chains import (
    OptionsChainsData,
    OptionsChainsQueryParams,
)
from openbb_core.provider.utils.errors import OpenBBError
from pydantic import Field, field_validator

from openbb_platform.providers.ibkr.openbb_ibkr.utils import IBKRConnectionSingleton

load_dotenv()

# Set up environment variables with defaults
IBKR_ACCOUNT_MODE = os.getenv("IBKR_ACCOUNT_MODE", "paper")
IBKR_SNAPSHOT = int(os.getenv("IBKR_SNAPSHOT", "1"))  # "1" for snapshot, "0" for streaming
IBKR_MARKET_DATA_TYPE = int(os.getenv("IBKR_MARKET_DATA_TYPE", "1"))  # 1 for real-time data

class IBKROptionsChainsQueryParams(OptionsChainsQueryParams):
    """IBKR Options Chains Query.

    source: https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option

    This class defines the necessary attributes for querying options data
    through the IBKR API, based on ib_async's Option class.

    Attributes:
        symbol (str): The underlying asset symbol (required).
        lastTradeDateOrContractMonth (str): The option's last trading day or contract month.
            YYYYMM format: To specify last month
            YYYYMMDD format: To specify last trading day
        right (str): The type of option: "C" or "CALL" for call, "P" or "PUT" for put (required).
        strike (float): The strike price of the option (required).
        exchange (Optional[str]): The exchange code for the option (optional).
        currency (str): The currency in which the option is traded (optional, default: "USD").
        multiplier (str): The contract multiplier, usually 100 for options (100)
    """

    __alias_dict__ = {
        "symbol": "underlying",
        "expiry": "expiry",
        "right": "type",
        "strike": "strike",
        "exchange": "exchange",
        "multiplier": "multiplier",
        "currency": "currency"
    }

    symbol: str = Field(alias="underlying")
    expiry: str = Field(
        alias="lastTradeDateOrContractMonth",
        description="Specify as 'YYYYMM' for contract month or 'YYYYMMDD' for last trading day."
    )
    right: Literal["C", "P", "CALL", "PUT"] = Field(alias="right")
    strike: float = Field(alias="strike")
    exchange: Optional[str] = Field(None, alias="exchange")
    currency: str = Field("USD", alias="currency")  # Default to USD, if applicable
    multiplier: str = Field(alias="multiplier")

    @field_validator("right", pre=True, check_fields=False)
    def validate_right(cls, v):
        if v in {"CALL", "PUT"}:
            return v[0]  # Convert to 'C' or 'P' if in long form
        if v in {"C", "P"}:
            return v
        raise ValueError("Invalid value for 'right'. Use 'C', 'P', 'CALL', or 'PUT'.")

    @field_validator("expiry", pre=True, check_fields=False)
    def validate_expiry(cls, v):
        if len(v) == 6:  # YYYYMM format for contract month
            datetime.strptime(v, "%Y%m")
        elif len(v) == 8:  # YYYYMMDD format for last trading day
            datetime.strptime(v, "%Y%m%d")
        else:
            raise ValueError("Invalid format for 'expiry'. Use 'YYYYMM' or 'YYYYMMDD'.")
        return v

class IBKROptionsChainsData(OptionsChainsData):
    """IBKR Options Chains Data."""

    __doc__ = OptionsChainsData.__doc__
    __alias_dict__ = {
        "symbol": "symbol",
        "expiry": "lastTradeDateOrContractMonth",  # Expiration date format from IBKR
        "strike": "strike",
        "right": "right",
        "exchange": "exchange",
        "multiplier": "multiplier",
        "trading_class": "tradingClass",
        "bid": "bidPrice",
        "ask": "askPrice",
        "last": "lastPrice",
        "volume": "volume",
        "open_interest": "openInterest",
    }

    # Define fields matching the aliases
    # symbol: str
    # expiry: datetime
    # strike: float
    # right: Literal["C", "P"]
    # exchange: Optional[str]
    # multiplier: float
    # trading_class: str
    # bid: Optional[float]
    # ask: Optional[float]
    # last: Optional[float]
    # volume: Optional[int]
    # open_interest: Optional[int]

class IBKROptionsChainsFetcher(
    Fetcher[IBKROptionsChainsQueryParams, IBKROptionsChainsData]
):
    """IBKR Options Chains Fetcher."""

    def __init__(self):
        # Set up environment variables with defaults
        self.account_mode = os.getenv("IBKR_ACCOUNT_MODE", "paper")
        self.snapshot = int(os.getenv("IBKR_SNAPSHOT", "1"))  # "1" for snapshot, "0" for streaming
        self.market_data_type = int(os.getenv("IBKR_MARKET_DATA_TYPE", "1"))  # 1 for real-time data

        # Initialize the singleton connection
        self.ibkr_connection = IBKRConnectionSingleton()

    async def set_market_data_type(self):
        """
        Sets the market data type for the IBKR connection.
        Market data types: 1 for real-time, 2 for frozen, 3 for delayed, 4 for delayed frozen.
        """
        await self.ibkr_connection.ib.reqMarketDataType(self.market_data_type)

    async def fetch_options_chain(self, symbol: str, exchange: str, expiry: str, strike: float, right: str):
        """
        Fetch options chain data for a specific symbol.

        :param symbol: The underlying symbol for the option
        :param exchange: The exchange on which the option is listed
        :param expiry: Expiration date in 'YYYYMMDD' format
        :param strike: Strike price of the option
        :param right: 'C' for Call, 'P' for Put
        :return: Options data as received from IBKR
        """
        # Define the option contract
        contract = Option(symbol=symbol, exchange=exchange, expiry=expiry, strike=strike, right=right)

        # Request market data using the snapshot setting
        ticker = await self.ibkr_connection.ib.reqMktData(contract, snapshot=self.snapshot)

        # Extract data, e.g., bid/ask prices, greeks if available
        options_data = {
            "symbol": symbol,
            "bid": ticker.bid,
            "ask": ticker.ask,
            "last": ticker.last,
            "greeks": {
                "delta": ticker.bidGreeks.delta if ticker.bidGreeks else None,
                "gamma": ticker.bidGreeks.gamma if ticker.bidGreeks else None,
                "theta": ticker.bidGreeks.theta if ticker.bidGreeks else None,
                "vega": ticker.bidGreeks.vega if ticker.bidGreeks else None
            }
        }
        return options_data

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> IBKROptionsChainsQueryParams:
        """Transform the query."""
        return IBKROptionsChainsQueryParams(**params)
