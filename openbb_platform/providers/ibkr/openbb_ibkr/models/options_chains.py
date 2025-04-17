"""IBKR Options Chains Model."""

import asyncio
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
from openbb_ibkr.utils.helpers import normalize_result_data
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
        "expiration": "lastTradeDateOrContractMonth",
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
    def parse_expiration(cls, value: list[Any]) -> list[datetime]:
        """Convert the expiration date format to a proper datetime object."""
        parsed = []

        for v in value:
            if v is None:
                parsed.append(None)
            elif isinstance(v, str):
                if len(v) == 6:
                    parsed.append(datetime.strptime(v, "%Y%m"))
                elif len(v) == 8:
                    parsed.append(datetime.strptime(v, "%Y%m%d"))
                else:
                    raise ValueError(f"Invalid expiration format: {v}")
            elif isinstance(v, datetime):
                parsed.append(v)
            else:
                raise TypeError(f"Unsupported type for expiration: {type(v)}")

        return parsed


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

        update_event = asyncio.Event()

        def on_update(_ticker):
            """Callback function to trigger event when new data arrives."""
            update_event.set()


        # generic_tick_list = "100,101,104,106,165,221,233"
        generic_tick_list = "100,101,104,106,165,221,233,236,258,293,294,295,375,411,456,588"
        ticker = IBKROptionsChainsFetcher.ibkr_connection.ib.reqMktData(
            contract, genericTickList=generic_tick_list,
            snapshot=IBKROptionsChainsFetcher.snapshot
        )

        ticker.updateEvent.connect(listener=on_update)

        try:
            await asyncio.wait_for(update_event.wait(), timeout=10)
        except asyncio.TimeoutError:
            raise TimeoutError(f"Timed out waiting for market data for {query.symbol}.")
        finally:
            ticker.updateEvent.disconnect(on_update)

        ticker_data = {
            attr: getattr(ticker, attr, None)
            for attr in dir(ticker)
            if not attr.startswith("_") and not callable(getattr(ticker, attr, None))
        }


        result_data = {
            "underlying_symbol": query.symbol,
            "contract_symbol": ticker_data.get("localSymbol"),
            "expiration": ticker_data.get("lastTradeDateOrContractMonth"),
            "strike": query.strike,
            "option_type": query.right,
            "bid": (ticker_data.get("bid")),
            "ask": (ticker_data.get("ask")),
            "last": (ticker_data.get("last")),
            "implied_volatility": (ticker_data.get("impliedVolatility")),
            "open_interest": (
                ticker_data.get("callOpenInterest") if query.right == "C" else ticker_data.get("putOpenInterest")
            ),
            "volume": (
                ticker_data.get("callVolume") if query.right == "C" else ticker_data.get("putVolume")
            ),
        }

        result_data = normalize_result_data(result_data)

        metadata_data: Dict[str, Any] = {
            key: value
            for key, value in ticker_data.items()
            if key not in result_data
        }

        return AnnotatedResult(
            result=IBKROptionsChainsData(**result_data),
            metadata=metadata_data
        )


    @staticmethod
    def transform_data(
        query: IBKROptionsChainsQueryParams,
        data: AnnotatedResult,
        **kwargs,
    ) -> AnnotatedResult[IBKROptionsChainsData]:
        return data
