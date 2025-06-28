from typing import Any, Generator

import pytest
from openbb_ibkr.utils.helpers import openbb_dry_run


@pytest.fixture(autouse=True)
def _openbb_dry_run() -> Generator[None, Any, None]:
    # Every test runs with static-asset writes disabled
    with openbb_dry_run():
        yield
