# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Web framework integration.

Provides web framework integration and HTTP handling for FLEXT applications.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

from flext_web.__version__ import (
    VERSION,
    FlextWebVersion,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
    _VersionMetadata,
)

if _TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_web.api import *
    from flext_web.base import *
    from flext_web.constants import *
    from flext_web.models import *
    from flext_web.protocols import *
    from flext_web.services import *
    from flext_web.settings import *
    from flext_web.typings import *
    from flext_web.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("flext_web.services",),
    {
        "FlextWeb": "flext_web.api",
        "FlextWebConstants": "flext_web.constants",
        "FlextWebModels": "flext_web.models",
        "FlextWebProtocols": "flext_web.protocols",
        "FlextWebServiceBase": "flext_web.base",
        "FlextWebSettings": "flext_web.settings",
        "FlextWebTypes": "flext_web.typings",
        "FlextWebUtilities": "flext_web.utilities",
        "api": "flext_web.api",
        "base": "flext_web.base",
        "c": ("flext_web.constants", "FlextWebConstants"),
        "constants": "flext_web.constants",
        "d": "flext_core",
        "e": "flext_core",
        "h": "flext_core",
        "m": ("flext_web.models", "FlextWebModels"),
        "models": "flext_web.models",
        "p": ("flext_web.protocols", "FlextWebProtocols"),
        "protocols": "flext_web.protocols",
        "r": "flext_core",
        "s": "flext_core",
        "services": "flext_web.services",
        "settings": "flext_web.settings",
        "t": ("flext_web.typings", "FlextWebTypes"),
        "typings": "flext_web.typings",
        "u": ("flext_web.utilities", "FlextWebUtilities"),
        "utilities": "flext_web.utilities",
        "web": "flext_web.api",
        "x": "flext_core",
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "FlextWebVersion",
        "VERSION",
        "_VersionMetadata",
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
