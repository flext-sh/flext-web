"""Unit tests for flext_web.version module.

Tests the version management functionality following flext standards.
"""

from __future__ import annotations

from flext_tests import u

from flext_web.__version__ import (
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
    u.Tests.Matchers.that(isinstance(__version__, str), eq=True)
    u.Tests.Matchers.that(isinstance(__version_info__, tuple), eq=True)
    u.Tests.Matchers.that(len(__version_info__) > 0, eq=True)
    u.Tests.Matchers.that(isinstance(VERSION, FlextWebVersion), eq=True)


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
            )
        )
        u.Tests.Matchers.that(version.version, eq="1.0.0")
        u.Tests.Matchers.that(version.version_info, eq=(1, 0, 0))

    def test_current_version(self) -> None:
        """Test current version retrieval."""
        current = FlextWebVersion.current()
        u.Tests.Matchers.that(isinstance(current.version, str), eq=True)
        u.Tests.Matchers.that(isinstance(current.version_info, tuple), eq=True)
        u.Tests.Matchers.that(len(current.version_info) > 0, eq=True)

    def test_version_globals(self) -> None:
        """Test global version variables."""
        assert_version_info()
        u.Tests.Matchers.that(VERSION.version, eq=__version__)
        u.Tests.Matchers.that(VERSION.version_info, eq=__version_info__)

    def test_version_format(self) -> None:
        """Test version format is valid."""
        version_parts = __version__.split(".")
        u.Tests.Matchers.that(len(version_parts) >= 2, eq=True)
        version_from_info = ".".join(str(part) for part in __version_info__)
        u.Tests.Matchers.that(version_from_info, eq=__version__)

    def test_metadata_constants(self) -> None:
        """Test that metadata constants are properly defined."""
        u.Tests.Matchers.that(isinstance(__title__, str), eq=True)
        u.Tests.Matchers.that(isinstance(__description__, str), eq=True)
        u.Tests.Matchers.that(isinstance(__author__, str), eq=True)
        u.Tests.Matchers.that(isinstance(__author_email__, str), eq=True)
        u.Tests.Matchers.that(isinstance(__license__, str), eq=True)
        u.Tests.Matchers.that(isinstance(__url__, str), eq=True)
        u.Tests.Matchers.that(len(__title__) > 0, eq=True)
        u.Tests.Matchers.that(len(__description__) > 0, eq=True)
        u.Tests.Matchers.that(len(__author__) > 0, eq=True)
        u.Tests.Matchers.that(isinstance(__license__, str), eq=True)
        if __url__:
            u.Tests.Matchers.that(
                "://" in __url__ or __url__.startswith("http"), eq=True
            )
