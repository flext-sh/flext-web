"""FLEXT Web Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, NotRequired, TypedDict

from flext_cli import t, u

from flext_web.constants import c
from flext_web.models import m


class FlextWebTypes(t):
    """Web-specific type definitions extending t via MRO."""

    class Web:
        """Web domain namespace (flat members per AGENTS.md §149)."""

        class CreateWebConfigKwargs(TypedDict, total=False):
            """Typed kwargs accepted by ``FlextWebSettings.create_web_config``."""

            host: NotRequired[str]
            port: NotRequired[t.PortNumber]
            debug: NotRequired[bool]
            secret_key: NotRequired[str]

        class ApplicationConfig(m.Web.EntityConfig):
            """Application configuration with web-specific defaults."""

            name: Annotated[str, u.Field(description="App name")] = (
                c.Web.DEFAULT_APP_NAME
            )
            status: Annotated[str, u.Field(description="App status")] = (
                c.Web.Status.STOPPED.value
            )
            environment: Annotated[str, u.Field(description="Environment")] = (
                c.Web.Name.DEVELOPMENT.value
            )
            debug_mode: Annotated[bool, u.Field(description="Debug")] = (
                c.Web.DEFAULT_DEBUG_MODE
            )
            version: Annotated[int, u.Field(description="Version")] = (
                c.Web.DEFAULT_VERSION_INT
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
