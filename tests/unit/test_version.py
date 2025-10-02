"""Version metadata tests for flext-web."""

from __future__ import annotations

from collections.abc import Mapping

from flext_core.metadata import FlextProjectMetadata, FlextProjectPerson

from flext_web import __version__, __version_info__
from flext_web.version import VERSION, FlextWebVersion


def test_dunder_alignment() -> None:
    """Ensure __version__ mirrors VERSION."""
    assert __version__ == VERSION.version
    assert __version_info__ == VERSION.version_info


def test_metadata_view() -> None:
    """VERSION exposes normalized metadata from pyproject."""
    assert isinstance(VERSION, FlextWebVersion)
    assert isinstance(VERSION.metadata, FlextProjectMetadata)
    assert isinstance(VERSION.urls, Mapping)
    assert VERSION.version_info == VERSION.version_tuple


def test_metadata_contacts() -> None:
    """Primary contacts are available as FlextProjectPerson instances."""
    assert isinstance(VERSION.author, FlextProjectPerson)
    assert isinstance(VERSION.maintainer, FlextProjectPerson)
    assert VERSION.author_name
    assert VERSION.maintainer_name


def test_metadata_passthrough() -> None:
    """Author and maintainer collections match the metadata dataclass."""
    assert VERSION.authors == VERSION.metadata.authors
    assert VERSION.maintainers == VERSION.metadata.maintainers
