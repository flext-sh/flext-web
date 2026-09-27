"""FLEXT Web constants."""

from __future__ import annotations

from flext_cli import FlextCliConstants, t

from ._constants.base import FlextWebConstantsBase
from ._constants.values import FlextWebConstantsValues


class FlextWebConstants(FlextCliConstants):
    """Immutable project-specific constants organized by domain."""

    class Web(FlextWebConstantsBase, FlextWebConstantsValues):
        """Web domain constants namespace."""


c = FlextWebConstants

__all__: t.StrSequence = ("FlextWebConstants", "c")
