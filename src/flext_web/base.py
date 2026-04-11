"""Shared service foundation for flext-web components.

Centralizes typed access to the registered `web` settings namespace while
preserving the flext-core service lifecycle and logger/runtime inheritance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import override

from pydantic import Field

from flext_core import FlextSettings, s, t
from flext_web import FlextWebSettings


class FlextWebServiceBase[TDomainResult: t.ValueOrModel | Sequence[t.ValueOrModel]](
    s[TDomainResult],
    ABC,
):
    """Base class for flext-web services with typed `web` settings access."""

    config_type: type | None = Field(
        default=FlextWebSettings, description="Settings class for web services"
    )

    @property
    @override
    def settings(self) -> FlextWebSettings:
        """Return the typed settings bound to this service runtime."""
        settings = self.settings
        if self.config_overrides is not None and isinstance(settings, FlextWebSettings):
            return settings
        return FlextSettings.fetch_global().fetch_namespace("web", FlextWebSettings)


__all__ = ["FlextWebServiceBase"]
