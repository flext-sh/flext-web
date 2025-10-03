"""Version metadata for flext web."""

from __future__ import annotations

from importlib.metadata import metadata
from typing import Final

_metadata = metadata("flext-web")

__version__: Final[str] = _metadata["Version"]
__version_info__: Final[tuple[int | str, ...]] = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)

__all__ = ["__version__", "__version_info__"]
