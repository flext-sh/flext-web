"""Package version and metadata information.

Provides version information and package metadata using standard library
metadata extraction.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import metadata
from typing import Final

from pydantic import BaseModel, ConfigDict, Field

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


class _VersionMetadata(BaseModel):
    """Version metadata model for constructor."""

    model_config = ConfigDict(frozen=False, extra="forbid")

    version: str = Field(default="")
    version_info: tuple[int | str, ...] = Field(default=())
    title: str = Field(default="")
    description: str = Field(default="")
    author: str = Field(default="")
    author_email: str = Field(default="")
    license_type: str = Field(default="")
    url: str = Field(default="")


class FlextWebVersion:
    """Structured package metadata.

    Provides metadata access through singleton pattern using importlib.metadata.
    """

    def __init__(self, metadata: _VersionMetadata) -> None:
        """Initialize version metadata.

        Args:
            metadata: Version metadata model

        """
        super().__init__()
        self.version = metadata.version
        self.version_info = metadata.version_info
        self.title = metadata.title
        self.description = metadata.description
        self.author = metadata.author
        self.author_email = metadata.author_email
        self.license = metadata.license_type
        self.url = metadata.url

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
            ),
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
