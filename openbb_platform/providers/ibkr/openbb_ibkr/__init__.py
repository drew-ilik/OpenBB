"""Interactive Brokers Provider Module."""

from openbb_core.provider.abstract.provider import Provider


template_provider = Provider(
    name="ibkr",
    website="https://interactivebrokers.com",
    description=("""The Interactive Brokers (IBKR) provider allows users to fetch real-time
        and historical data directly from the Interactive Brokers API. It is
        designed to support a variety of assets including stocks, options, futures,
        and forex, integrating seamlessly with OpenBB."""
    ),
    fetcher_dict = {},
)

def setup_ibkr_provider():
    """Setup any necessary configuration for the IBKR provider."""
    pass
