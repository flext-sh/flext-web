"""Base helpers for flext-web models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_cli import t, u
from flext_web import c


class FlextWebModelsBase:
    """Shared model helpers for flext-web model namespaces."""

    _METHOD_ADAPTER: ClassVar[u.TypeAdapter[c.Web.Method]] = u.TypeAdapter(
        c.Web.Method,
    )

    @classmethod
    def coerce_method(cls, value: t.Scalar) -> c.Web.Method:
        """Coerce user-provided HTTP method values into the Web method enum."""
        normalized_value = value.upper() if isinstance(value, str) else value
        return cls._METHOD_ADAPTER.validate_python(normalized_value)


__all__: list[str] = ["FlextWebModelsBase"]
