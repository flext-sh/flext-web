"""Authentication and data payload models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import m, u
from flext_web import c, t


class FlextWebModelsAuth:
    """Authentication and payload models namespace."""

    class Web:
        """Authentication and data payload models."""

        class Credentials(m.Value):
            """Authentication credentials model."""

            username: Annotated[str, u.Field(min_length=1, description="Username")]
            password: Annotated[str, u.Field(min_length=1, description="Password")]

        class UserData(m.Value):
            """User registration data model."""

            username: Annotated[str, u.Field(min_length=1, description="Username")]
            email: Annotated[str, u.Field(min_length=1, description="Email address")]
            password: Annotated[
                str,
                u.Field(
                    description="Password (empty string if not provided)",
                ),
            ] = ""

        class AppData(m.Value):
            """Application creation data model."""

            name: Annotated[
                str,
                u.Field(
                    min_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[0],
                    max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                    description="Application name",
                ),
            ]
            host: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SECURITY_MAX_HOST_LENGTH,
                    description="Application host",
                ),
            ]
            port: Annotated[
                t.PortNumber,
                u.Field(
                    ...,
                    description="Application port",
                ),
            ]

        class EntityData(m.Value):
            """Generic entity data model."""

            data: Annotated[
                t.MutableConfigurationMapping,
                u.Field(
                    description="Entity data dictionary",
                ),
            ] = u.Field(default_factory=dict)


__all__: list[str] = ["FlextWebModelsAuth"]
