"""Authentication and data payload models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated

from flext_cli import m

from flext_web import c, t


class FlextWebModelsAuth:
    """Authentication and data payload models."""

    class Credentials(m.Value):
        """Authentication credentials model."""

        username: Annotated[str, m.Field(min_length=1, description="Username")]
        password: Annotated[str, m.Field(min_length=1, description="Password")]

    class UserData(m.Value):
        """User registration data model."""

        username: Annotated[str, m.Field(min_length=1, description="Username")]
        email: Annotated[str, m.Field(min_length=1, description="Email address")]
        password: Annotated[
            str,
            m.Field(description="Password (empty string if not provided)"),
        ] = ""

    class AppData(m.Value):
        """Application creation data model."""

        name: Annotated[
            str,
            m.Field(
                min_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[0],
                max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                description="Application name",
            ),
        ]
        host: Annotated[
            str,
            m.Field(
                min_length=1,
                max_length=c.Web.SECURITY_MAX_HOST_LENGTH,
                description="Application host",
            ),
        ]
        port: Annotated[t.PortNumber, m.Field(..., description="Application port")]

    class EntityData(m.Value):
        """Generic entity data model."""

        data: Annotated[
            t.ConfigurationMapping,
            m.Field(description="Entity data dictionary"),
        ] = m.Field(default_factory=lambda: MappingProxyType[str, t.Scalar]({}))


__all__: list[str] = ["FlextWebModelsAuth"]
