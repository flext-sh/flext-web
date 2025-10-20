"""Package metadata - Canonical single source of truth (Layer 0: Pure Constants).

Uses importlib.metadata to fetch version and package information from pyproject.toml.
Provides both simple module-level constants and structured FlextWebVersion class
following flext-core patterns for consistent access patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import metadata
from typing import Final

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
__url__: Final[str] = _metadata["Home-Page"]


class FlextWebVersion:
    """Structured package metadata following flext-core patterns.

    Provides canonical metadata access through singleton pattern.
    All data comes from pyproject.toml via importlib.metadata.

    Example:
        >>> version = FlextWebVersion.current()
        >>> print(version.version)  # "0.9.0"
        >>> print(version.version_info)  # (0, 9, 0)

    """

    def __init__(
        self,
        version: str,
        version_info: tuple[int | str, ...],
        title: str,
        description: str,
        author: str,
        author_email: str,
        license_type: str,
        url: str,
    ) -> None:
        """Initialize version metadata.

        Args:
            version: Package version string
            version_info: Parsed version tuple
            title: Package title
            description: Package description
            author: Package author name
            author_email: Package author email
            license_type: License identifier
            url: Package URL

        """
        super().__init__()
        self.version = version
        self.version_info = version_info
        self.title = title
        self.description = description
        self.author = author
        self.author_email = author_email
        self.license = license_type
        self.url = url

    @classmethod
    def current(cls) -> FlextWebVersion:
        """Return current package metadata from pyproject.toml.

        Returns:
            FlextWebVersion: Current package metadata

        """
        return cls(
            version=__version__,
            version_info=__version_info__,
            title=__title__,
            description=__description__,
            author=__author__,
            author_email=__author_email__,
            license_type=__license__,
            url=__url__,
        )


VERSION: Final[FlextWebVersion] = FlextWebVersion.current()


__all__ = [
    "VERSION",
    "FlextWebVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
