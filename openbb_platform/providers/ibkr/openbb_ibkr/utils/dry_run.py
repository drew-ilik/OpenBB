"""Utility module for dry run operations in OpenBB package building."""
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator

import openbb_core.app.static.package_builder as _pb_mod

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(handler)

project_root = Path(__file__).parents[2] / "openbb"

@contextmanager
def openbb_dry_run(*, verbose: bool = True) -> Generator[None, Any, None]:
    """
    Context manager to temporarily replace the PackageBuilder with a dry-run version,
    without writing any files.
    """
    OrigBuilder = _pb_mod.PackageBuilder

    class DryBuilder(OrigBuilder):
        def auto_build(self):
            logger.info("Dry run build started …")
            super().auto_build()
            logger.info("Dry run complete (no files changed).")

        def _write(self, path: Path, content: str) -> None:
            """
            Instead of writing the file, log the intended write operation with optional verbose output.
            """
            if self.verbose:
                rel = path.relative_to(Path.cwd())
                logger.info(f"[dry-run] would write: {rel}")


    _pb_mod.PackageBuilder = DryBuilder
    try:
        yield
    finally:
        # Restore the original PackageBuilder after the context
        _pb_mod.PackageBuilder = OrigBuilder
        if verbose:
            logger.info("Restored original PackageBuilder.")

