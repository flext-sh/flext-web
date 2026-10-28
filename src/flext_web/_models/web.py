"""Extracted facade class for web.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web._models._web import FlextWebModelsWebMessage, FlextWebModelsWebRequest


class FlextWebModelsWeb(
    FlextWebModelsWebMessage,
    FlextWebModelsWebRequest,
):
    """Facade for web."""


__all__: list[str] = ["FlextWebModelsWeb"]
