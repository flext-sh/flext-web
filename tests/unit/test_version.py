"""Unit tests for flext_web.version module.

Tests the version management functionality following flext standards.
"""

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
    assert isinstance(__version__, str)
    assert isinstance(__version_info__, tuple)
    assert len(__version_info__) > 0
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

        assert version.version == "1.0.0"
        assert version.version_info == (1, 0, 0)

    def test_current_version(self) -> None:
        """Test current version retrieval."""
        current = FlextWebVersion.current()

        assert isinstance(current.version, str)
        assert isinstance(current.version_info, tuple)
        assert len(current.version_info) > 0

    def test_version_globals(self) -> None:
        """Test global version variables."""
        assert_version_info()

        # Verify consistency
        assert VERSION.version == __version__
        assert VERSION.version_info == __version_info__

    def test_version_format(self) -> None:
        """Test version format is valid."""
        version_parts = __version__.split(".")
        assert len(version_parts) >= 2  # At least major.minor

        # Check that version_info matches version string
        version_from_info = ".".join(str(part) for part in __version_info__)
        assert version_from_info == __version__

    def test_metadata_constants(self) -> None:
        """Test that metadata constants are properly defined."""
        # Test that all metadata constants are strings
        assert isinstance(__title__, str)
        assert isinstance(__description__, str)
        assert isinstance(__author__, str)
        assert isinstance(__author_email__, str)
        assert isinstance(__license__, str)
        assert isinstance(__url__, str)

        # Test that they are not empty
        assert len(__title__) > 0
        assert len(__description__) > 0
        assert len(__author__) > 0
        assert isinstance(__license__, str)

        # Test reasonable URL format (optional)
        if __url__:
            assert "://" in __url__ or __url__.startswith("http")
