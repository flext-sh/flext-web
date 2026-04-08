# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.constants import TestsFlextWebConstants, TestsFlextWebConstants as c
    from tests.helpers.models import TestsModels
    from tests.helpers.protocols import TestsProtocols
    from tests.helpers.typings import TestsTypings
    from tests.helpers.utilities import TestsUtilities
    from tests.models import TestsFlextWebModels, TestsFlextWebModels as m
    from tests.protocols import TestsFlextWebProtocols, TestsFlextWebProtocols as p
    from tests.typings import TestsFlextWebTypes, TestsFlextWebTypes as t
    from tests.utilities import TestsFlextWebUtilities, TestsFlextWebUtilities as u
_LAZY_IMPORTS = merge_lazy_imports(
    ("tests.helpers",),
    {
        "TestsFlextWebConstants": ("tests.constants", "TestsFlextWebConstants"),
        "TestsFlextWebModels": ("tests.models", "TestsFlextWebModels"),
        "TestsFlextWebProtocols": ("tests.protocols", "TestsFlextWebProtocols"),
        "TestsFlextWebTypes": ("tests.typings", "TestsFlextWebTypes"),
        "TestsFlextWebUtilities": ("tests.utilities", "TestsFlextWebUtilities"),
        "c": ("tests.constants", "TestsFlextWebConstants"),
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("tests.models", "TestsFlextWebModels"),
        "p": ("tests.protocols", "TestsFlextWebProtocols"),
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": ("tests.typings", "TestsFlextWebTypes"),
        "u": ("tests.utilities", "TestsFlextWebUtilities"),
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "TestsFlextWebConstants",
    "TestsFlextWebModels",
    "TestsFlextWebProtocols",
    "TestsFlextWebTypes",
    "TestsFlextWebUtilities",
    "TestsModels",
    "TestsProtocols",
    "TestsTypings",
    "TestsUtilities",
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
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
