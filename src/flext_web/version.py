"""Project metadata for flext web."""

from __future__ import annotations

from importlib.metadata import metadata
from typing import Final

_metadata = metadata("flext-web")

__version__: Final[str] = _metadata["Version"]
__version_info__: Final[tuple[int | str, ...]] = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)


class FlextWebVersion:
    """Structured metadata for the flext web distribution."""

    def __init__(self, version: str, version_info: tuple[int | str, ...]) -> None:
        """Initialize version metadata."""
        self.version = version
        self.version_info = version_info

    @classmethod
    def current(cls) -> FlextWebVersion:
        """Return canonical metadata loaded from pyproject.toml."""
        return cls(__version__, __version_info__)


VERSION: Final[FlextWebVersion] = FlextWebVersion.current()

for _name in tuple(_metadata):
    if _name not in {"__version__", "__version_info__"}:
        globals().pop(_name, None)

__all__ = ["VERSION", "FlextWebVersion", "__version__", "__version_info__"]
