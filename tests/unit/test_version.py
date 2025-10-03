"""Version metadata tests for flext-web."""

from __future__ import annotations

from flext_web import __version__, __version_info__
from flext_web.version import VERSION, FlextWebVersion


def test_dunder_alignment() -> None:
    """Ensure __version__ mirrors VERSION."""
    assert __version__ == VERSION.version
    assert __version_info__ == VERSION.version_info


def test_version_instance() -> None:
    """VERSION is a FlextWebVersion instance with correct attributes."""
    assert isinstance(VERSION, FlextWebVersion)
    assert hasattr(VERSION, "version")
    assert hasattr(VERSION, "version_info")
    assert isinstance(VERSION.version, str)
    assert isinstance(VERSION.version_info, tuple)
