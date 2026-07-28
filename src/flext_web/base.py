"""Shared service foundation for flext-web components.

Centralizes typed access to the registered `web` settings namespace while
preserving the flext-core service lifecycle and logger/runtime inheritance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC
from typing import ClassVar, override

from flext_core import FlextService
from flext_web import FlextWebSettings


class FlextWebServiceBase(FlextService[bool], ABC):
    """Base class for flext-web services with typed `web` settings access."""

    _settings_type: ClassVar[type[FlextWebSettings]] = FlextWebSettings

    @property
    @override
    def settings(self) -> FlextWebSettings:
        """Typed web settings bound to this runtime (falls back to the global)."""
        runtime = self.runtime_settings
        if runtime is not None:
            return FlextWebSettings.model_validate(runtime)
        return FlextWebSettings.fetch_global()


s = FlextWebServiceBase

__all__: list[str] = ["FlextWebServiceBase", "s"]
