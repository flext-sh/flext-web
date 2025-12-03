"""Package metadata - Canonical single source of truth (Layer 0: Pure Constants).

Uses importlib.metadata to fetch version and package information from pyproject.toml.
Provides both simple module-level constants and structured FlextWebVersion class
following flext-core patterns for consistent access patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import metadata
from typing import Final, TypedDict

_metadata = metadata("flext-web")

__version__: Final[str] = _metadata["Version"]
__version_info__: Final[tuple[int | str, ...]] = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)
__title__: Final[str] = _metadata["Name"]
__description__: Final[str] = _metadata["Summary"]
__author__: Final[str] = _metadata["Author"]
__author_email__: Final[str] = _metadata["Author-Email"]
__license__: Final[str] = _metadata["License"]
__url__: Final[str] = _metadata.get("Home-Page", "")


class _VersionMetadata(TypedDict):
    """Version metadata dictionary for constructor."""

    version: str
    version_info: tuple[int | str, ...]
    title: str
    description: str
    author: str
    author_email: str
    license_type: str
    url: str


class FlextWebVersion:
    """Structured package metadata following flext-core patterns.

    Provides canonical metadata access through singleton pattern.
    All data comes from pyproject.toml via importlib.metadata.

    Example:
        >>> version = FlextWebVersion.current()
        >>> print(version.version)  # "0.9.0"
        >>> print(version.version_info)  # (0, 9, 0)

    """

    def __init__(self, metadata: _VersionMetadata) -> None:
        """Initialize version metadata.

        Args:
            metadata: Version metadata dictionary

        """
        super().__init__()
        self.version = metadata["version"]
        self.version_info = metadata["version_info"]
        self.title = metadata["title"]
        self.description = metadata["description"]
        self.author = metadata["author"]
        self.author_email = metadata["author_email"]
        self.license = metadata["license_type"]
        self.url = metadata["url"]

    @classmethod
    def current(cls) -> FlextWebVersion:
        """Return current package metadata from pyproject.toml.

        Returns:
            FlextWebVersion: Current package metadata

        """
        return cls(
            _VersionMetadata(
                version=__version__,
                version_info=__version_info__,
                title=__title__,
                description=__description__,
                author=__author__,
                author_email=__author_email__,
                license_type=__license__,
                url=__url__,
            )
        )


VERSION: Final[FlextWebVersion] = FlextWebVersion.current()


__all__ = [
    "VERSION",
    "FlextWebVersion",
    "_VersionMetadata",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
