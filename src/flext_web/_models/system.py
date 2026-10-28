"""System, health, and runtime models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Annotated

from flext_cli import m


class FlextWebModelsSystem:
    """System, health, and runtime models."""

    class SystemInfo(m.BaseModel):
        """System information response model."""

        service_name: Annotated[str, m.Field(description="Service name")]
        service_type: Annotated[str, m.Field(description="Service type")]
        architecture: Annotated[str, m.Field(description="Architecture pattern")]
        patterns: Annotated[Sequence[str], m.Field(description="Design patterns used")]
        integrations: Annotated[
            Sequence[str],
            m.Field(description="Integrated components"),
        ]
        capabilities: Annotated[
            Sequence[str],
            m.Field(description="Service capabilities"),
        ]

    class HealthStatus(m.BaseModel):
        """Health status response model."""

        status: Annotated[str, m.Field(description="Health status")]
        service: Annotated[str, m.Field(description="Service name")]
        version: Annotated[str, m.Field(description="Service version")]
        timestamp: Annotated[str, m.Field(description="Status timestamp")]
        components: Annotated[
            Mapping[str, str], m.Field(description="Component statuses")
        ]


__all__: list[str] = ["FlextWebModelsSystem"]
