"""Base constants for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final


class FlextWebConstantsBase:
    """Base constants for flext-web."""

    VALIDATION_NAME_LENGTH_RANGE: Final[tuple[int, int]] = (3, 100)
    SECURITY_MAX_DESCRIPTION_LENGTH: Final[int] = 500
    API_DOCS_URL: Final[str] = "/docs"
    API_REDOC_URL: Final[str] = "/redoc"
    API_OPENAPI_URL: Final[str] = "/openapi.json"
    API_DEFAULT_DESCRIPTION: Final[str] = "Generic HTTP Service"


__all__: list[str] = ["FlextWebConstantsBase"]
