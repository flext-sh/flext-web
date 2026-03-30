"""Unit tests for flext_web.version module.

Tests the version management functionality following flext standards.
"""

from __future__ import annotations

from flext_tests import tm

from flext_web import (
    VERSION,
    FlextWebVersion,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
    _VersionMetadata,
)


def assert_version_info() -> None:
    """Helper to assert version info is valid."""
    tm.that(__version__, is_=str)
    tm.that(__version_info__, is_=tuple)
    tm.that(__version_info__, empty=False)
    assert isinstance(VERSION, FlextWebVersion)


class TestFlextWebVersion:
    """Test suite for FlextWebVersion class."""

    def test_version_initialization(self) -> None:
        """Test FlextWebVersion initialization."""
        version = FlextWebVersion(
            _VersionMetadata(
                version="1.0.0",
                version_info=(1, 0, 0),
                title="FLEXT Web",
                description="Generic HTTP Service",
                author="FLEXT Team",
                author_email="flext@example.com",
                license_type="MIT",
                url="https://github.com/flext/flext-web",
            ),
        )
        tm.that(version.version, eq="1.0.0")
        tm.that(version.version_info, eq=(1, 0, 0))

    def test_current_version(self) -> None:
        """Test current version retrieval."""
        current = FlextWebVersion.current()
        tm.that(current.version, is_=str)
        tm.that(current.version_info, is_=tuple)
        tm.that(current.version_info, empty=False)

    def test_version_globals(self) -> None:
        """Test global version variables."""
        assert_version_info()
        tm.that(VERSION.version, eq=__version__)
        tm.that(VERSION.version_info, eq=__version_info__)

    def test_version_format(self) -> None:
        """Test version format is valid."""
        version_parts = __version__.split(".")
        tm.that(len(version_parts), gte=2)
        version_from_info = ".".join(str(part) for part in __version_info__)
        tm.that(version_from_info, eq=__version__)

    def test_metadata_constants(self) -> None:
        """Test that metadata constants are properly defined."""
        tm.that(__title__, is_=str)
        tm.that(__description__, is_=str)
        tm.that(__author__, is_=str)
        tm.that(__author_email__, is_=str)
        tm.that(__license__, is_=str)
        tm.that(__url__, is_=str)
        tm.that(__title__, empty=False)
        tm.that(__description__, empty=False)
        tm.that(__license__, is_=str)
        if __url__:
            tm.that("://" in __url__ or __url__.startswith("http"), eq=True)
