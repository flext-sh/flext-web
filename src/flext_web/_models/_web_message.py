"""Web application request/response models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid
from typing import Annotated

from flext_cli import u
from flext_web import c, p, r, t

from ._http import FlextWebModelsHttp


class FlextWebModelsWebMessage:
    """Web application message models namespace."""

    class Web:
        """Web application request/response models."""

        class AppRequest(FlextWebModelsHttp.Web.Request):
            """Web request entity with tracking and context information.

            Extends generic HTTP request with web application-specific fields
            for request tracking, client identification, and analysis.

            Attributes:
                url: Request URL
                method: HTTP method
                timeout: Request timeout
                headers: HTTP headers
                body: Message body
                timestamp: Request timestamp
                request_id: Unique request identifier
                query_params: Query string parameters
                client_ip: Client IP address
                user_agent: Client user agent string

            """

            request_id: Annotated[
                str,
                u.Field(
                    description="Unique request identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            query_params: Annotated[
                t.MutableConfigurationMapping,
                u.Field(
                    description="Query string parameters",
                ),
            ] = u.Field(default_factory=dict)
            client_ip: Annotated[
                str,
                u.Field(description="Client IP address"),
            ] = ""
            user_agent: Annotated[
                str,
                u.Field(description="Client user agent"),
            ] = ""

            @classmethod
            def create_web_request(
                cls,
                settings: FlextWebModelsWebMessage.Web.AppRequest,
            ) -> p.Result[FlextWebModelsWebMessage.Web.AppRequest]:
                """Re-validate an :class:`AppRequest` snapshot."""
                return r[FlextWebModelsWebMessage.Web.AppRequest].create_from_callable(
                    lambda: cls.model_validate(settings),
                )

        class AppResponse(FlextWebModelsHttp.Web.Response):
            """Web response entity with tracking and performance metrics.

            Extends generic HTTP response with web application-specific fields
            for response tracking, performance monitoring, and client context.

            Attributes:
                status_code: HTTP status code
                headers: HTTP response headers
                body: Response body content
                timestamp: Response timestamp
                elapsed_time: Response processing time
                response_id: Unique response identifier
                request_id: Associated request identifier
                content_type: Response content type
                content_length: Response body length in bytes
                processing_time_ms: Processing time in milliseconds

            """

            elapsed_time: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Response elapsed time in seconds",
                ),
            ] = 0.0
            response_id: Annotated[
                str,
                u.Field(
                    description="Unique response identifier",
                ),
            ] = u.Field(default_factory=lambda: str(uuid.uuid4()))
            request_id: Annotated[
                str,
                u.Field(description="Associated request identifier"),
            ]
            content_type: Annotated[
                str,
                u.Field(
                    description="Response content type",
                ),
            ] = c.Web.HTTP_CONTENT_TYPE_JSON
            content_length: Annotated[
                t.NonNegativeInt,
                u.Field(
                    description="Response body length in bytes",
                ),
            ] = 0
            processing_time_ms: Annotated[
                t.NonNegativeFloat,
                u.Field(
                    description="Processing time in milliseconds",
                ),
            ] = 0.0

            @property
            def processing_time_seconds(self) -> float:
                """Convert processing time from milliseconds to seconds.

                Returns:
                    Processing time in seconds

                """
                processing_time_seconds: float = self.processing_time_ms / 1000
                return processing_time_seconds

            @classmethod
            def create_web_response(
                cls,
                settings: FlextWebModelsWebMessage.Web.AppResponse,
            ) -> p.Result[FlextWebModelsWebMessage.Web.AppResponse]:
                """Re-validate an :class:`AppResponse` snapshot."""
                return r[FlextWebModelsWebMessage.Web.AppResponse].create_from_callable(
                    lambda: cls.model_validate(settings),
                )


__all__: list[str] = ["FlextWebModelsWebMessage"]
