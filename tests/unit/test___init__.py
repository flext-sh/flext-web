"""Unit tests for the flext_web package public surface.

Tests assert observable behavior: the declared public export contract, the real
relationship between version string and version tuple, and that the canonical
`web` surface actually executes. Empty tests, facade-only type/callable checks,
and no-op loops are prohibited and absent.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import flext_web
from flext_tests import tm
from flext_web import __version__, __version_info__, web

if TYPE_CHECKING:
    from tests import t


class TestsFlextWebInit:
    """Behavior tests for flext_web package initialization."""

    def test_version_string_matches_version_info(self) -> None:
        """__version__ is the dotted join of the numeric __version_info__ parts."""
        numeric_prefix = ".".join(str(part) for part in __version_info__)
        tm.that(__version__.startswith(numeric_prefix), eq=True)

    def test_all_exports_match(self) -> None:
        """The declared __all__ export set is exactly the public contract."""
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
            "settings",
            "t",
            "u",
            "web",
            "x",
        }
        module_all: t.StrSequence = getattr(flext_web, "__all__", [])
        tm.that(set(module_all), eq=expected_exports)

    def test_public_web_surface_executes(self) -> None:
        """The `web` facade actually runs a real operation end to end."""
        health = web.health_status()
        tm.ok(health)
        tm.that(health.value.service, eq="flext-web")

    def test_facade_aliases_resolve_to_real_namespaces(self) -> None:
        """Each alias resolves and exposes its Web namespace attribute."""
        for alias_name in ("c", "t", "p", "m", "u"):
            alias = getattr(flext_web, alias_name)
            tm.that(hasattr(alias, "Web"), eq=True)
