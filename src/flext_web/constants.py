"""FLEXT Web Constants - Domain-specific constants (eliminando duplicações com flext-core).

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Enhanced web domain-specific constants extending FlextConstants.

    Contains comprehensive constants for FLEXT web applications with
    enhanced organization, validation limits, and security considerations.
    """


__all__ = [
    "FlextWebConstants",
]
