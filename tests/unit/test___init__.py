"""Unit tests for flext_web.__init__ module.

Tests the package initialization and exports.
"""

import flext_web
from flext_web.__version__ import __version__, __version_info__


class TestFlextWebInit:
    """Test suite for flext_web package initialization."""

    def test_package_imports(self) -> None:
        """Test that all main classes are importable from package."""
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
        assert isinstance(__version__, str)
        assert isinstance(__version_info__, tuple)

    def test_all_exports_match(self) -> None:
        """Test that __all__ contains all expected exports."""
        expected_exports = {
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
            "_ApplicationConfig",
            "_WebRequestConfig",
            "_WebResponseConfig",
            "__all__",
            "c",
            "create_app",
            "h",
            "list_apps",
            "m",
            "p",
            "start_app",
            "stop_app",
            "t",
            "u",
        }
        assert set(flext_web.__all__) == expected_exports

    def test_imports_are_classes_or_modules(self) -> None:
        """Test that imported items are of correct types."""
        assert callable(flext_web.FlextWebApi)
        assert callable(flext_web.FlextWebSettings)
        assert isinstance(__version__, str)
