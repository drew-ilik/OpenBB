import pytest


def pytest_collection_modifyitems(config, items) -> None:
    """Skip @pytest.mark.record_http for IBKR tests."""
    for item in items:
        if "record_http" in item.keywords:
            item.keywords.pop("record_http", None)
            item.add_marker(pytest.mark.no_http_record)


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "no_http_record: IBKR uses sockets. HTTP recording disabled for these tests.",
    )
