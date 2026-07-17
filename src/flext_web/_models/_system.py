"""System, health, and runtime models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, ClassVar, TYPE_CHECKING


from flext_cli import m, u
from flext_web import t

if TYPE_CHECKING:
    from wsgiref.simple_server import WSGIServer
    import uvicorn
    from threading import Thread


class FlextWebModelsSystem:
    """System, health, and runtime models namespace."""

    class Web:
        """System, health, and runtime models."""

        class SystemInfo(m.BaseModel):
            """System information response model."""

            service_name: Annotated[str, u.Field(description="Service name")]
            service_type: Annotated[str, u.Field(description="Service type")]
            architecture: Annotated[str, u.Field(description="Architecture pattern")]
            patterns: Annotated[
                t.StrSequence, u.Field(description="Design patterns used")
            ]
            integrations: Annotated[
                t.StrSequence, u.Field(description="Integrated components")
            ]
            capabilities: Annotated[
                t.StrSequence, u.Field(description="Service capabilities")
            ]

        class HealthStatus(m.BaseModel):
            """Health status response model."""

            status: Annotated[str, u.Field(description="Health status")]
            service: Annotated[str, u.Field(description="Service name")]
            version: Annotated[str, u.Field(description="Service version")]
            timestamp: Annotated[str, u.Field(description="Status timestamp")]
            components: Annotated[
                t.StrMapping, u.Field(description="Component statuses")
            ]

        class AppRuntimeInfo(m.ArbitraryTypesModel):
            """Runtime information for a running web application.

            Tracks the server instance, daemon thread, and runner type
            for each started application so it can be stopped cleanly.
            """

            model_config: ClassVar[t.ConfigDict] = t.ConfigDict(
                arbitrary_types_allowed=True, frozen=True, extra="forbid"
            )
            runner: Annotated[
                str, u.Field(description="Runtime runner name (uvicorn, werkzeug)")
            ]
            server: Annotated[
                uvicorn.Server | WSGIServer,
                u.Field(description="Server instance for lifecycle management"),
            ]
            thread: Annotated[
                Thread, u.Field(description="Daemon thread running the server")
            ]


__all__: list[str] = ["FlextWebModelsSystem"]
