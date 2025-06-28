"""IBKR Provider Helpers"""
import logging
import math
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Optional

import openbb
from openbb_core.app.static.package_builder import PackageBuilder

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

class DryRunPackageBuilder(PackageBuilder):
    """A PackageBuilder subclass that intercepts file writes for a dry-run rebuild with verbose output."""

    def __init__(
            self,
            project_dir: Path,
            lint: bool = True,
            verbose: bool = False,
            **kwargs: Any,
        ):
        super().__init__(project_dir, lint, verbose, **kwargs)
        self.verbose = verbose

    def _write_file(self, path: Path, content: str) -> None:
        """
        Instead of writing the file, log the intended write operation with optional verbose output.
        """
        if self.verbose:
            rel = path.relative_to(Path.cwd())
            logger.info("[dry-run] would write: %s", rel)
        # do *not* call super()._write_file

    def build(self, modules=None):
        if self.verbose:
            logger.info("Dry-run build started …")
        super().build(modules)
        if self.verbose:
            logger.info("Dry-run complete (no files changed).")

@contextmanager
def openbb_dry_run() -> Generator[None, Any, None]:
    """
    Context manager to temporarily replace the PackageBuilder with DryRunPackageBuilder,
    enabling a dry-run of the static asset rebuild.
    """
    original_cls = openbb._PackageBuilder
    openbb._PackageBuilder = DryRunPackageBuilder
    try:
        yield
    finally:
        openbb._PackageBuilder = original_cls

def fetch_and_cache(self, symbol):
    if symbol in self.cache:
        return self.cache[symbol]
    data = self.connection.ib.reqMktData(symbol)
    self.cache[symbol] = data
    return data

def is_live_account(account_mode: str) -> bool:
    """Check if the current account mode is live or paper."""
    return account_mode == "live"

def normalize_result_data(raw: dict[str, Any]) -> dict[str, list[Any]]:
    """Normalize raw ticker data for use in OpenBB fetchers."""

    def process_value(v: Any) -> Any:
        if isinstance(v, float) and math.isnan(v):
            return None
        return v

    return {
        k: (
            v if isinstance(v, list)
            else [process_value(v)] if v is not None
            else []
        )
        for k, v in raw.items()
    }

def safe_getattr(obj: Any, attr: str, default: Optional[Any]=None) -> Any:
    try:
        return getattr(obj, attr, default)
    except Exception:
        return default
