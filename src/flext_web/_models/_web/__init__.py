# AUTO-GENERATED FILE — Regenerate with: make gen
"""Internal package for web.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._models._web.message import FlextWebModelsWebMessage
    from flext_web._models._web.request import FlextWebModelsWebRequest

__all__: tuple[str, ...] = (
    "FlextWebModelsWebMessage",
    "FlextWebModelsWebRequest",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextWebModelsWebMessage": ".message",
        "FlextWebModelsWebRequest": ".request",
    }),
    public_exports=__all__,
)
