"""IBKR Options Chains Model."""

# pylint: disable=unused-argument
from datetime import (
    date as dateType,
    datetime,
)
from typing import Any, Dict, List, Literal, Optional
from warnings import warn

from openbb_core.provider.abstract.fetcher import Fetcher
from openbb_core.provider.standard_models.options_chains import (
    OptionsChainsData,
    OptionsChainsQueryParams,
)
from openbb_core.provider.utils.errors import OpenBBError
from pydantic import Field, field_validator


class IBKROptionsChainsQueryParams(OptionsChainsQueryParams):
    """IBKR Options Chains Query.

    source:
    """

    __alias_dict__ = {
    }

class IBKROptionsChainsData(OptionsChainsData):
    """IBKR Options Chains Data."""

    __doc__ = OptionsChainsData.__doc__
    __alias_dict__ = {
    }

class IBKROptionsChainsFetcher(
    Fetcher[IBKROptionsChainsQueryParams, IBKROptionsChainsData]
):
    """IBKR Options Chains Fetcher."""

    @staticmethod
    def transform_query(params: Dict[str, Any]) -> IBKROptionsChainsQueryParams:
        """Transform the query."""
        return IBKROptionsChainsQueryParams(**params)
