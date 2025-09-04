"""Tests for version information."""

from __future__ import annotations


def test_version_import() -> None:
    """Test that version can be imported."""
    from flext_web.__version__ import __version__
    assert isinstance(__version__, str)
    assert __version__ == "0.9.0"


def test_version_all_export() -> None:
    """Test __all__ export."""
    from flext_web.__version__ import __all__
    assert __all__ == ["__version__"]