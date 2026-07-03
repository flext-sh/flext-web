"""Base helpers for flext-web models.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import t, u
from flext_web.constants import c

_METHOD_ADAPTER = u.TypeAdapter(c.Web.Method)


def _coerce_method(v: t.Scalar) -> c.Web.Method:
    if isinstance(v, str):
        v = v.upper()
    return _METHOD_ADAPTER.validate_python(v)


__all__: list[str] = ["_coerce_method"]
