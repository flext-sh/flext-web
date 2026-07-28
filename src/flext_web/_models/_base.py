"""Base helpers for flext-web models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_web import c, t


class FlextWebModelsBase:
    """Shared model helpers for flext-web model namespaces."""

    @classmethod
    def coerce_method(cls, value: t.Scalar) -> c.Web.Method:
        """Coerce user-provided HTTP method values into the Web method enum."""
        normalized_value = value.upper() if isinstance(value, str) else value
        return c.Web.Method(normalized_value)


__all__: list[str] = ["FlextWebModelsBase"]
