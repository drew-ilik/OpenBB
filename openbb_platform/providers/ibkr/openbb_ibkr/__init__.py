"""Interactive Brokers Provider Module."""

from openbb_core.provider.abstract.provider import Provider

from .models.options_chains import IBKROptionsChainsFetcher

ibkr_provider = Provider(
    name="ibkr",
    website="https://interactivebrokers.com",
    description=("""The Interactive Brokers (IBKR) provider allows users to fetch real-time
        and historical data directly from the Interactive Brokers API. It is
        designed to support a variety of assets including stocks, options, futures,
        and forex, integrating seamlessly with OpenBB."""
    ),
    fetcher_dict = {
        "options_chains": IBKROptionsChainsFetcher,
    },
)
