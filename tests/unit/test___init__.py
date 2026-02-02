"""Unit tests for flext_web.__init__ module.

Tests the package initialization and exports.
"""

import flext_web


class TestFlextWebInit:
    """Test suite for flext_web package initialization."""

    def test_package_imports(self) -> None:
        """Test that all main classes are importable from package."""
        # Test that all __all__ exports are available
        assert hasattr(flext_web, "FlextWebApi")
        assert hasattr(flext_web, "FlextWebApp")
        assert hasattr(flext_web, "FlextWebSettings")
        assert hasattr(flext_web, "FlextWebConstants")
        assert hasattr(flext_web, "FlextWebHandlers")
        assert hasattr(flext_web, "FlextWebModels")
        assert hasattr(flext_web, "FlextWebProtocols")
        assert hasattr(flext_web, "FlextWebServices")
        assert hasattr(flext_web, "FlextWebTypes")
        assert hasattr(flext_web, "FlextWebUtilities")

    def test_version_exports(self) -> None:
        """Test that version information is exported."""
        assert hasattr(flext_web, "__version__")
        assert hasattr(flext_web, "__version_info__")
        assert isinstance(flext_web.__version__, str)
        assert isinstance(flext_web.__version_info__, tuple)

    def test_all_exports_match(self) -> None:
        """Test that __all__ contains all expected exports."""
        expected_exports = {
            # Main classes
            "FlextWebApi",
            "FlextWebApp",
            "FlextWebSettings",
            "FlextWebConstants",
            "FlextWebHandlers",
            "FlextWebModels",
            "FlextWebProtocols",
            "FlextWebServices",
            "FlextWebTypes",
            "FlextWebUtilities",
            # Version info
            "__version__",
            "__version_info__",
            # Short aliases (FLEXT namespace pattern)
            "c",  # FlextWebConstants alias
            "m",  # FlextWebModels alias
            "p",  # FlextWebProtocols alias
            "t",  # FlextWebTypes alias
            "u",  # FlextWebUtilities alias
        }

        assert set(flext_web.__all__) == expected_exports

    def test_imports_are_classes_or_modules(self) -> None:
        """Test that imported items are of correct types."""
        # Test that main classes are classes
        assert callable(flext_web.FlextWebApi)  # Should be callable class
        assert callable(flext_web.FlextWebSettings)  # Should be callable class

        # Test that version is string
        assert isinstance(flext_web.__version__, str)
