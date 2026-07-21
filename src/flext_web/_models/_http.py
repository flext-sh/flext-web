"""HTTP message models for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_cli import m, p, u
from flext_web import c, r, t

from ._base import FlextWebModelsBase

if TYPE_CHECKING:
    from datetime import datetime


class FlextWebModelsHttp:
    """HTTP message models namespace."""

    class Web:
        """HTTP message models for HTTP protocol entities."""

        class Message(m.Value):
            """Generic HTTP message base model with protocol validation.

            Represents common HTTP message structure with headers, body,
            and timestamp. Used as base for Request and Response models.

            Attributes:
                headers: HTTP headers dictionary mapping header names to values
                body: Message body as string, dict, or None for no body
                timestamp: Timestamp when message was created (configured timezone)

            """

            headers: Annotated[
                t.MutableStrMapping, u.Field(description="HTTP headers for message")
            ] = u.Field(default_factory=dict)
            body: Annotated[
                str | t.ScalarMapping | None,
                u.Field(description="Message body content (optional for GET/HEAD)"),
            ] = None
            timestamp: Annotated[
                datetime,
                u.Field(
                    description="Timestamp of message creation (configured timezone)"
                ),
            ] = u.Field(default_factory=u.now)

        class Request(Message):
            """HTTP request model with complete validation.

            Represents a complete HTTP request following HTTP specifications
            with full validation of URL, method, and timeout parameters.

            Attributes:
            url: Request URL with length validation
            method: HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
            timeout: Request timeout in seconds (0-300)

            """

            url: Annotated[
                str,
                u.Field(
                    min_length=1,
                    max_length=c.Web.VALIDATION_URL_LENGTH_RANGE[1],
                    description="Request URL",
                ),
            ]
            method: Annotated[
                c.Web.Method,
                u.PlainValidator(FlextWebModelsBase.coerce_method),
                u.Field(
                    description="HTTP method (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)"
                ),
            ] = c.Web.Method.GET
            timeout: Annotated[
                t.PositiveTimeout, u.Field(description="Request timeout in seconds")
            ] = c.Web.DEFAULT_TIMEOUT_SECONDS

            @property
            def has_body(self) -> bool:
                """Whether HTTP request has a message body.

                Returns:
                True if body is not None, False otherwise

                """
                return self.body is not None

            @property
            def secure(self) -> bool:
                """Whether HTTP request uses HTTPS protocol.

                Returns:
                True if URL starts with 'https://', False otherwise

                """
                return self.url.startswith("https://")

            @classmethod
            def create_http_request(
                cls,
                url: str,
                method: str = c.Web.Method.GET,
                headers: t.StrMapping | None = None,
                body: str | t.MappingKV[str, t.Scalar] | None = None,
                timeout: float = c.Web.DEFAULT_TIMEOUT_SECONDS,
            ) -> p.Result[FlextWebModelsHttp.Web.Request]:
                """Build a validated :class:`Request` from raw HTTP parameters."""
                return r[FlextWebModelsHttp.Web.Request].create_from_callable(
                    lambda: cls.model_validate({
                        "url": url,
                        "method": method,
                        "headers": dict(headers or {}),
                        "body": body,
                        "timeout": timeout,
                    })
                )

        class Response(Message):
            """HTTP response model with status validation.

            Represents a complete HTTP response with status code validation
            and response-specific properties.

            Attributes:
            status_code: HTTP status code (100-599)
            elapsed_time: Time taken to process response in seconds

            """

            status_code: Annotated[
                t.HttpStatusCode, u.Field(..., description="HTTP status code")
            ]
            elapsed_time: Annotated[
                t.NonNegativeFloat | None,
                u.Field(description="Response processing time in seconds"),
            ] = None

            @property
            def error(self) -> bool:
                """Whether HTTP status indicates client or server error.

                Returns:
                    True if status_code >= c.ERROR_MIN, False otherwise

                """
                has_error: bool = self.status_code >= c.Web.ERROR_MIN
                return has_error

            @property
            def success(self) -> bool:
                """Whether HTTP status indicates success (2xx range).

                Returns:
                    True if status code in range(*c.SUCCESS_RANGE), False otherwise

                """
                success_min, success_max = c.Web.SUCCESS_RANGE
                is_success: bool = success_min <= self.status_code <= success_max
                return is_success

            @classmethod
            def create_http_response(
                cls,
                status_code: int,
                headers: t.StrMapping | None = None,
                body: str | t.MappingKV[str, t.Scalar] | None = None,
                elapsed_time: float | None = None,
            ) -> p.Result[FlextWebModelsHttp.Web.Response]:
                """Build a validated :class:`Response` from raw HTTP fields."""
                return r[FlextWebModelsHttp.Web.Response].create_from_callable(
                    lambda: cls.model_validate({
                        "status_code": status_code,
                        "headers": dict(headers or {}),
                        "body": body,
                        "elapsed_time": elapsed_time,
                    })
                )


__all__: list[str] = ["FlextWebModelsHttp"]
