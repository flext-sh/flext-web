"""Configuration models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_web import c, m, t, u


class FlextWebModelsConfig:
    """Web configuration models namespace."""

    class Web:
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
                middlewares: List of middleware objects to apply
                docs_url: Swagger UI docs URL
                redoc_url: ReDoc URL
                openapi_url: OpenAPI schema URL

            """

            title: Annotated[
                str,
                u.Field(
                    min_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[0],
                    max_length=c.Web.VALIDATION_NAME_LENGTH_RANGE[1],
                    description="FastAPI application title",
                ),
            ] = c.Web.DEFAULT_APP_NAME
            version: Annotated[
                str,
                u.Field(
                    description="Application version",
                ),
            ] = c.Web.DEFAULT_VERSION_STRING
            description: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.SECURITY_MAX_DESCRIPTION_LENGTH,
                    description="Application description",
                ),
            ] = c.Web.API_DEFAULT_DESCRIPTION
            debug: Annotated[
                bool,
                u.Field(description="FastAPI debug mode"),
            ] = False
            testing: Annotated[
                bool,
                u.Field(description="FastAPI testing mode"),
            ] = False
            middlewares: Annotated[
                t.StrSequence,
                u.Field(
                    description="List of middleware objects",
                ),
            ] = u.Field(default_factory=list)
            docs_url: Annotated[
                str,
                u.Field(
                    description="Documentation URL",
                ),
            ] = c.Web.API_DOCS_URL
            redoc_url: Annotated[
                str,
                u.Field(
                    description="ReDoc URL",
                ),
            ] = c.Web.API_REDOC_URL
            openapi_url: Annotated[
                str,
                u.Field(
                    description="OpenAPI URL",
                ),
            ] = c.Web.API_OPENAPI_URL


__all__: list[str] = ["FlextWebModelsConfig"]
