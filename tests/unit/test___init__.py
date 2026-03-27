"""Unit tests for flext_web.__init__ module.

Tests the package initialization and exports.
"""

from flext_tests import tm

import flext_web
from flext_web.__version__ import __version__, __version_info__


class TestFlextWebInit:
    """Test suite for flext_web package initialization."""

    _WEB_SURFACE = (
        "create_fastapi_app",
        "create_flask_app",
        "authenticate",
        "register_user",
        "create_entity",
        "get_entity",
        "list_entities",
        "health_status",
        "dashboard_metrics",
        "dashboard",
        "create_app",
        "get_app",
        "list_apps",
        "start_app",
        "stop_app",
        "start_service",
        "stop_service",
        "initialize_routes",
        "configure_middleware",
        "handle_system_info",
        "handle_health_check",
    )

    def test_package_imports(self) -> None:
        """Test that all main classes are importable from package."""
        tm.that(hasattr(flext_web, "FlextWeb"), eq=True)
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
        tm.that(__version__, is_=str)
        tm.that(__version_info__, is_=tuple)

    def test_all_exports_match(self) -> None:
        """Test that __all__ contains all expected exports."""
        expected_exports = {
            "FlextWeb",
            "FlextWebApp",
            "FlextWebSettings",
            "FlextWebConstants",
            "FlextWebAuth",
            "FlextWebEntities",
            "FlextWebHandlers",
            "FlextWebHealth",
            "FlextWebModels",
            "FlextWebProtocols",
            "FlextWebServiceBase",
            "FlextWebServices",
            "FlextWebTypes",
            "FlextWebUtilities",
            "__all__",
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "services",
            "t",
            "u",
            "web",
            "x",
        }
        assert set(flext_web.__all__) == expected_exports

    def test_imports_are_classes_or_modules(self) -> None:
        """Test that imported items are of correct types."""
        tm.that(callable(flext_web.FlextWeb), eq=True)
        tm.that(callable(flext_web.FlextWebSettings), eq=True)
        tm.that(__version__, is_=str)

    def test_web_and_aliases_define_the_public_surface(self) -> None:
        """The package exposes the canonical `web, c, t, p, m, u` surface."""
        for name in self._WEB_SURFACE:
            tm.that(hasattr(flext_web.web, name), eq=True)
        for alias_name in ("c", "t", "p", "m", "u"):
            alias = getattr(flext_web, alias_name)
            tm.that(hasattr(alias, "Web"), eq=True)
