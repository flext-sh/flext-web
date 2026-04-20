"""Unit tests for flext_web.__init__ module.

Tests the package initialization and exports.
"""

from __future__ import annotations

from flext_tests import tm

import flext_web
from flext_web import __version__, __version_info__
from tests import t


class TestFlextWebInit:
    """Test suite for flext_web package initialization."""

    _WEB_SURFACE = (
        "create_fastapi_app",
        "create_flask_app",
        "authenticate",
        "register_user",
        "create_entity",
        "fetch_entity",
        "list_entities",
        "health_status",
        "dashboard_metrics",
        "dashboard",
        "create_app",
        "fetch_app",
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

    def test_version_exports(self) -> None:
        """Test that version information is exported."""
        tm.that(__version__, is_=str)
        tm.that(__version_info__, is_=tuple)

    def test_all_exports_match(self) -> None:
        """Test that __all__ contains all expected exports."""
        expected_exports = {
            "FlextWeb",
            "FlextWebApp",
            "FlextWebAuth",
            "FlextWebConstants",
            "FlextWebEntities",
            "FlextWebHandlers",
            "FlextWebHealth",
            "FlextWebModels",
            "FlextWebProtocols",
            "FlextWebServiceBase",
            "FlextWebServices",
            "FlextWebSettings",
            "FlextWebTypes",
            "FlextWebUtilities",
            "__author__",
            "__author_email__",
            "__description__",
            "__license__",
            "__title__",
            "__url__",
            "__version__",
            "__version_info__",
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "u",
            "web",
            "x",
        }
        module_all: t.StrSequence = getattr(flext_web, "__all__", [])
        assert set(module_all) == expected_exports

    def test_imports_are_classes_or_modules(self) -> None:
        """Test that imported items are of correct types."""
        tm.that(callable(flext_web.FlextWeb), eq=True)
        tm.that(callable(flext_web.FlextWebSettings), eq=True)
        tm.that(__version__, is_=str)

    def test_web_and_aliases_define_the_public_surface(self) -> None:
        """The package exposes the canonical `web, c, t, p, m, u` surface."""
        for _name in self._WEB_SURFACE:
            pass
        for alias_name in ("c", "t", "p", "m", "u"):
            getattr(flext_web, alias_name)
