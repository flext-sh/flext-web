"""FLEXT Web utilities facade."""

from __future__ import annotations

from flext_cli import u

from flext_web import t

from ._utilities.base import FlextWebUtilitiesBase
from ._utilities.web import FlextWebUtilitiesWeb


class FlextWebUtilities(u):
    """Web-specific utilities delegating to flext-core.

    Inherits from u and ensures consistency.
    Provides only web-domain-specific functionality not available in u.
    All generic operations delegate to flext-core utilities.
    Uses advanced builder/DSL patterns for composition.
    """

    class Web(FlextWebUtilitiesBase, FlextWebUtilitiesWeb):
        """Web domain-specific runtime utilities."""


u = FlextWebUtilities

__all__: t.MutableSequenceOf[str] = ["FlextWebUtilities", "u"]
