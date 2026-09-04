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
        # A method is a string token; any other scalar is compared by its text
        # form and rejected by the enum when it names no method.
        normalized_value = (value if isinstance(value, str) else str(value)).upper()
        return c.Web.Method(normalized_value)


__all__: list[str] = ["FlextWebModelsBase"]
