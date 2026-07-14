"""Shared service foundation for flext-web components.

Centralizes typed access to the registered `web` settings namespace while
preserving the flext-core service lifecycle and logger/runtime inheritance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC

from flext_core import FlextService


class FlextWebServiceBase(FlextService[bool], ABC):
    """Base class for flext-web services with typed `web` settings access."""


s = FlextWebServiceBase

__all__: list[str] = ["FlextWebServiceBase", "s"]
