"""FLEXT Web Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_cli import t

from flext_web import c, m, u


class FlextWebTypes(t):
    """Web-specific type definitions extending t via MRO."""

    class Web:
        """Web domain namespace (flat members per AGENTS.md §149)."""

        class ApplicationConfig(m.Web.EntityConfig):
            """Application configuration with web-specific defaults."""

            name: Annotated[str, u.Field(description="App name")] = (
                c.Web.WebDefaults.APP_NAME
            )
            status: Annotated[str, u.Field(description="App status")] = (
                c.Web.Status.STOPPED.value
            )
            environment: Annotated[str, u.Field(description="Environment")] = (
                c.Web.Name.DEVELOPMENT.value
            )
            debug_mode: Annotated[bool, u.Field(description="Debug")] = (
                c.Web.WebDefaults.DEBUG_MODE
            )
            version: Annotated[int, u.Field(description="Version")] = (
                c.Web.WebDefaults.VERSION_INT
            )

        class RequestConfig(m.Web.AppRequest):
            """Web request configuration extending AppRequest."""

        class ResponseConfig(m.Web.AppResponse):
            """Web response configuration extending AppResponse."""

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
