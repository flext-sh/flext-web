# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Helpers package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_web import models, protocols, typings, utilities
    from flext_web.models import TestsModels, TestsModels as m
    from flext_web.protocols import TestsProtocols, TestsProtocols as p
    from flext_web.typings import TestsTypings, t
    from flext_web.utilities import TestsUtilities, TestsUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestsModels": "flext_web.models",
    "TestsProtocols": "flext_web.protocols",
    "TestsTypings": "flext_web.typings",
    "TestsUtilities": "flext_web.utilities",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_web.models", "TestsModels"),
    "models": "flext_web.models",
    "p": ("flext_web.protocols", "TestsProtocols"),
    "protocols": "flext_web.protocols",
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": "flext_web.typings",
    "typings": "flext_web.typings",
    "u": ("flext_web.utilities", "TestsUtilities"),
    "utilities": "flext_web.utilities",
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
