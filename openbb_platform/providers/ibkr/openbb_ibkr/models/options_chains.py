"""IBKR Options Chains Model."""

import os
from datetime import datetime
from typing import Any, Dict, Literal, Optional

from dotenv import load_dotenv
from ib_async.contract import Option
from openbb_core.provider.abstract.annotated_result import AnnotatedResult
from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.options_chains import (
    OptionsChainsData,
    OptionsChainsQueryParams,
)
from openbb_ibkr.utils.connection import IBKRConnectionSingleton
from pydantic import Field, field_validator

# from openbb_core.provider.utils.errors import OpenBBError

load_dotenv()

# Set up environment variables with defaults
IBKR_ACCOUNT_MODE = os.getenv("IBKR_ACCOUNT_MODE", "paper")
IBKR_SNAPSHOT = int(os.getenv("IBKR_SNAPSHOT", "1"))  # "1" for snapshot, "0" for streaming
IBKR_MARKET_DATA_TYPE = int(os.getenv("IBKR_MARKET_DATA_TYPE", "1"))  # 1 for real-time data

class IBKROptionsChainsQueryParams(OptionsChainsQueryParams):
    """IBKR Options Chains Query.

    source: https://ib-api-reloaded.github.io/ib_async/api.html#ib_async.contract.Option

    Defines attributes for querying options data through the IBKR API.

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
        "lastTradeDateOrContractMonth": "expiry",
        "right": "type",
    }

    symbol: str = Field(alias="underlying")
    lastTradeDateOrContractMonth: str = Field(
        alias="expiry",
        description="Specify as 'YYYYMM' for contract month or 'YYYYMMDD' for last trading day."
    )
    right: Literal["C", "P", "CALL", "PUT"] = Field(alias="type")
    strike: float = Field(alias="strike")
    exchange: str = Field(default="SMART", alias="exchange")
    currency: str = Field(default="USD", alias="currency")
    multiplier: str = Field(alias="multiplier")

    @field_validator("right", mode="before", check_fields=False)
    def validate_right(cls, v):
        if v in {"CALL", "PUT"}:
            return v[0]
        if v in {"C", "P"}:
            return v
        raise ValueError("Invalid value for 'right'. Use 'C', 'P', 'CALL', or 'PUT'.")

    @field_validator("lastTradeDateOrContractMonth", mode ="before", check_fields=False)
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
        # Direct mappings
        "underlying_symbol": "symbol",
        "contract_symbol": "localSymbol",
        "expiration": "lastTradeDateOrContractMonth",  # Expiration date format from IBKR
        "option_type": "right",
        "last_trade_time": "lastTradeTime",

        # Fields that need calculation or to be fetched separately
        # "dte": None,
        # "open_interest": None,
        # "volume": None,
        # "last_trade_price": None,
        # "last_trade_size": None,
        # "implied_volatility": None,
    }

    @field_validator("expiration", mode="before")
    def parse_expiration(cls, value):
        """Convert the expiration date format to a proper datetime object."""
        try:
            # Handle both YYYYMM and YYYYMMDD formats
            if len(value) == 6:
                return datetime.strptime(value, "%Y%m")
            elif len(value) == 8:
                return datetime.strptime(value, "%Y%m%d")
        except ValueError:
            raise ValueError(f"Invalid expiration format: {value}")
        return value

class IBKROptionsChainsFetcher(
    Fetcher[IBKROptionsChainsQueryParams, IBKROptionsChainsData]
):
    """IBKR Options Chains Fetcher."""

    # Tell query executor that credentials are not required for this fetcher
    require_credentials = False

    # Set up environment variables with defaults
    account_mode = os.getenv("IBKR_ACCOUNT_MODE", "paper")
    snapshot = int(os.getenv("IBKR_SNAPSHOT", "1"))  # "1" for snapshot, "0" for streaming
    market_data_type = int(os.getenv("IBKR_MARKET_DATA_TYPE", "1"))  # 1 for real-time data

    # Initialize the singleton connection
    ibkr_connection = IBKRConnectionSingleton()

    async def set_market_data_type(self):
        """
        Sets the market data type for the IBKR connection.
        Market data types: 1 for real-time, 2 for frozen, 3 for delayed, 4 for delayed frozen.
        """
        await self.ibkr_connection.ib.reqMarketDataType(marketDataType=self.market_data_type)

    @staticmethod
    async def aextract_data(
        query: IBKROptionsChainsQueryParams,
        credentials: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> Dict:
        """Return the raw data from the IBKR connection."""

        contract = Option(
            symbol=query.symbol,
            lastTradeDateOrContractMonth=query.lastTradeDateOrContractMonth,
            strike=query.strike,
            right=query.right,
            exchange=query.exchange,
            multiplier = query.multiplier,
            currency=query.currency
        )

        # Fetch market data directly
        ticker = await IBKROptionsChainsFetcher.ibkr_connection.ib.reqMktData(contract, snapshot=IBKROptionsChainsFetcher.snapshot) # noqa: E501

        options_data = {
            "symbol": query.symbol,
            "bid": ticker.bid,
            "ask": ticker.ask,
            "last": ticker.last,
        }
        return options_data

    @staticmethod
    def transform_data(
        query: IBKROptionsChainsQueryParams,
        data: Dict,
        **kwargs,
    ) -> AnnotatedResult[IBKROptionsChainsData]:
        return AnnotatedResult(
            result=IBKROptionsChainsData(**data),
            metadata={"source": "IBKR", "query": query.model_dump()},
        )
