"""Base constants for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar


class FlextWebConstantsBase:
    """Base constants for flext-web."""

    VALIDATION_NAME_LENGTH_RANGE: ClassVar[tuple[int, int]] = (3, 100)
    SECURITY_MAX_DESCRIPTION_LENGTH: ClassVar[int] = 500
    API_DOCS_URL: ClassVar[str] = "/docs"
    API_REDOC_URL: ClassVar[str] = "/redoc"
    API_OPENAPI_URL: ClassVar[str] = "/openapi.json"
    API_DEFAULT_DESCRIPTION: ClassVar[str] = "Generic HTTP Service"


__all__: list[str] = ["FlextWebConstantsBase"]
