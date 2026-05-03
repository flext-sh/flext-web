"""FLEXT Web Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import t


class FlextWebTypes(t):
    """Web-specific type definitions extending t via MRO."""

    class Web:
        """Web domain namespace (flat members per AGENTS.md §149)."""

        type RequestDict = dict[
            str,
            t.Scalar | t.StrSequence | t.ConfigurationMapping,
        ]
        type ResponseDict = dict[
            str,
            t.Scalar | t.StrSequence | t.ConfigurationMapping,
        ]


t = FlextWebTypes

__all__: list[str] = [
    "FlextWebTypes",
    "t",
]
