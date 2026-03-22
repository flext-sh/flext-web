"""Unit tests for flext_web.__init__ module.

Tests the package initialization and exports.
"""

import flext_web
from flext_web.__version__ import __version__, __version_info__


class TestFlextWebInit:
    """Test suite for flext_web package initialization."""

    def test_package_imports(self) -> None:
        """Test that all main classes are importable from package."""
        tm.that(hasattr(flext_web, "FlextWebApi"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebApp"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebSettings"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebConstants"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebHandlers"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebModels"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebProtocols"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebServices"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebTypes"), eq=True)
        tm.that(hasattr(flext_web, "FlextWebUtilities"), eq=True)

    def test_version_exports(self) -> None:
        """Test that version information is exported."""
        tm.that(isinstance(__version__, str), eq=True)
        tm.that(isinstance(__version_info__, tuple), eq=True)

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
        tm.that(set(flext_web.__all__) == expected_exports, eq=True)

    def test_imports_are_classes_or_modules(self) -> None:
        """Test that imported items are of correct types."""
        tm.that(callable(flext_web.FlextWebApi), eq=True)
        tm.that(callable(flext_web.FlextWebSettings), eq=True)
        tm.that(isinstance(__version__, str), eq=True)
