"""System, health, and runtime models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, ClassVar

from flext_cli import m

if TYPE_CHECKING:
    from threading import Thread
    from wsgiref.simple_server import WSGIServer

    import uvicorn

    from flext_web import t


class FlextWebModelsSystem:
    """System, health, and runtime models."""

    class SystemInfo(m.BaseModel):
        """System information response model."""

        service_name: Annotated[str, m.Field(description="Service name")]
        service_type: Annotated[str, m.Field(description="Service type")]
        architecture: Annotated[str, m.Field(description="Architecture pattern")]
        patterns: Annotated[t.StrSequence, m.Field(description="Design patterns used")]
        integrations: Annotated[
            t.StrSequence,
            m.Field(description="Integrated components"),
        ]
        capabilities: Annotated[
            t.StrSequence,
            m.Field(description="Service capabilities"),
        ]

    class HealthStatus(m.BaseModel):
        """Health status response model."""

        status: Annotated[str, m.Field(description="Health status")]
        service: Annotated[str, m.Field(description="Service name")]
        version: Annotated[str, m.Field(description="Service version")]
        timestamp: Annotated[str, m.Field(description="Status timestamp")]
        components: Annotated[t.StrMapping, m.Field(description="Component statuses")]

    class AppRuntimeInfo(m.ArbitraryTypesModel):
        """Runtime information for a running web application.

        Tracks the server instance, daemon thread, and runner type
        for each started application so it can be stopped cleanly.
        """

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            arbitrary_types_allowed=True,
            frozen=True,
            extra="forbid",
        )
        runner: Annotated[
            str,
            m.Field(description="Runtime runner name (uvicorn, werkzeug)"),
        ]
        server: Annotated[
            uvicorn.Server | WSGIServer,
            m.Field(description="Server instance for lifecycle management"),
        ]
        thread: Annotated[
            Thread,
            m.Field(description="Daemon thread running the server"),
        ]


__all__: list[str] = ["FlextWebModelsSystem"]
