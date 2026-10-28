"""Configuration models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import Annotated

from flext_cli import m

from flext_web import c
from flext_web._settings import FlextWebSettings


class FlextWebModelsConfig:
    """Web configuration models."""

    class FastAPIAppConfig(m.BaseModel):
        """FastAPI application configuration model (Value Object).

        Represents FastAPI application configuration in Pydantic format
        for validation and type safety before passing to FastAPI.

        Attributes:
            title: FastAPI application title
            version: Application version
            description: Application description
            debug: Debug mode flag
            testing: Testing mode flag
            docs_url: Swagger UI docs URL
            redoc_url: ReDoc URL
            openapi_url: OpenAPI schema URL

        """

        title: Annotated[
            str,
            m.Field(
                # Resolve the current global singleton lazily (the module-level
                # `settings` capture goes stale when the singleton is replaced).
                default_factory=lambda: FlextWebSettings.fetch_global().Web.app_name,
                min_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[0],
                max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                description="FastAPI application title",
            ),
        ] = m.Field(
            default_factory=lambda: FlextWebSettings.fetch_global().Web.app_name,
        )
        version: Annotated[
            str,
            m.Field(
                default_factory=lambda: FlextWebSettings.fetch_global().Web.version,
                description="Application version",
            ),
        ] = m.Field(default_factory=lambda: FlextWebSettings.fetch_global().Web.version)
        description: Annotated[
            str,
            m.Field(
                min_length=1,
                max_length=c.Web.SECURITY_MAX_DESCRIPTION_LENGTH,
                description="Application description",
            ),
        ] = c.Web.API_DEFAULT_DESCRIPTION
        debug: Annotated[bool, m.Field(description="FastAPI debug mode")] = False
        testing: Annotated[bool, m.Field(description="FastAPI testing mode")] = False
        docs_url: Annotated[str, m.Field(description="Documentation URL")] = (
            c.Web.API_DOCS_URL
        )
        redoc_url: Annotated[str, m.Field(description="ReDoc URL")] = (
            c.Web.API_REDOC_URL
        )
        openapi_url: Annotated[str, m.Field(description="OpenAPI URL")] = (
            c.Web.API_OPENAPI_URL
        )


__all__: list[str] = ["FlextWebModelsConfig"]
