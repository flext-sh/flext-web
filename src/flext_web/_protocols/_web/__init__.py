# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Web. Protocols. Web package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_web._protocols._web.message import FlextWebProtocolsWebMessage
    from flext_web._protocols._web.request import FlextWebProtocolsWebRequest


__all__: tuple[str, ...] = (
    "FlextWebProtocolsWebMessage",
    "FlextWebProtocolsWebRequest",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextWebProtocolsWebMessage": ".message",
        "FlextWebProtocolsWebRequest": ".request",
    },
    public_exports=__all__,
)
