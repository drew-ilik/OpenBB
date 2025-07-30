from typing import Any, Generator

import pytest
from openbb_ibkr.utils import dry_run


@pytest.fixture(autouse=True)
def _openbb_dry_run() -> Generator[None, Any, None]:
    # Every test runs with static-asset writes disabled
    with dry_run.openbb_dry_run():
        yield
