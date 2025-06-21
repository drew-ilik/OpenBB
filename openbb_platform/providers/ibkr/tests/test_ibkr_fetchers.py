"""IBKR Fetchers tests."""

import inspect
from typing import get_args

import pandas as pd
import pytest
from openbb import obb
from openbb_core.app.service.user_service import UserService
from openbb_ibkr.models.options_chains import IBKROptionsChainsData, IBKROptionsChainsFetcher
from openbb_ibkr.utils.helpers import openbb_dry_run

test_credentials = UserService().default_user_settings.credentials.model_dump(
    mode="json"
)

@pytest.fixture(autouse=True)
def _dry_run():
    with openbb_dry_run():
        yield

# Provide dummy credentials / settings, if needed
@pytest.fixture(scope="module")
def sample_credentials():
    return {"account_mode": "live", "snapshot": False, "market_data_type": 3}

def test_chains_endpoint_provider():
    sig = inspect.signature(obb.derivatives.options.chains)
    provider_annotation = sig.parameters["provider"].annotation
    providers = get_args(provider_annotation)

    assert "ibkr" in providers, f"Expected 'ibkr' in providers, got {providers!r}"

# If you have a recorded VCR cassette:

# @pytest.mark.vcr()
# @pytest.mark.asyncio
# async def test_fetcher_returns_dataframe(sample_credentials):
#     fetcher = IBKROptionsChainsFetcher(credentials=sample_credentials)
#     df: pd.DataFrame = await fetcher.fetch("SPY")
#     # check columns
#     assert set(df.columns) >= {"contract_symbol", "expiration", "strike", "option_type"}
#     # check dtypes
#     assert isinstance(df.expiration.iloc[0], date)

# @pytest.fixture(scope="module")
# def vcr_config():
#     return {
#         "filter_headers": [
#             ("User-Agent", None),
#             ("api_key", "MOCK_API_KEY"),
#             ("x-api-token", "MOCK_API_KEY"),
#         ],
#         "filter_query_parameters": [
#             ("api_key", "MOCK_API_KEY"),
#             ("x-api-token", "MOCK_API_KEY"),
#         ],
#     }
