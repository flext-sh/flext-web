"""Web-domain type aliases for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import t


class FlextWebTypingsWeb:
    """Web-domain aliases composed into the public typings facade."""

    type RequestDict = dict[str, t.Scalar | t.StrSequence | t.ConfigurationMapping]
    type ResponseDict = dict[str, t.Scalar | t.StrSequence | t.ConfigurationMapping]
    type FastApiEndpointPayload = t.MappingKV[str, str | bool]


__all__: list[str] = ["FlextWebTypingsWeb"]
