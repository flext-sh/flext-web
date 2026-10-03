"""Unit tests for the flext_web package public surface.

Tests assert observable behavior: the declared public export contract, the real
relationship between version string and version tuple, and that the canonical
`web` surface actually executes. Empty tests, facade-only type/callable checks,
and no-op loops are prohibited and absent.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import tm

import flext_web
from flext_web import __version__, __version_info__, web

if TYPE_CHECKING:
    from tests import t


class TestsFlextWebInit:
    """Behavior tests for flext_web package initialization."""

    @staticmethod
    def test_version_string_matches_version_info() -> None:
        """__version__ is the dotted join of the numeric __version_info__ parts."""
        numeric_prefix = ".".join(str(part) for part in __version_info__)
        tm.that(__version__.startswith(numeric_prefix), eq=True)

    @staticmethod
    def test_all_exports_match() -> None:
        """__all__ is the generated contract: sorted, duplicate-free, every name resolves.

        The names themselves are a projection of what the package's modules
        declare (ADR-018); a test never freezes a projection's values, only its
        structure.
        """
        module_all: t.StrSequence = getattr(flext_web, "__all__", [])
        tm.that(list(module_all), eq=sorted(set(module_all)))
        tm.that(all(hasattr(flext_web, name) for name in module_all), eq=True)

    @staticmethod
    def test_public_web_surface_executes() -> None:
        """The `web` facade actually runs a real operation end to end."""
        health = web.health_status()
        tm.ok(health)
        tm.that(health.value.service, eq="flext-web")

    @staticmethod
    def test_facade_aliases_resolve_to_real_namespaces() -> None:
        """Each alias resolves and exposes its Web namespace attribute."""
        for alias_name in ("c", "t", "p", "m", "u"):
            alias = getattr(flext_web, alias_name)
            tm.that(hasattr(alias, "Web"), eq=True)
