"""FLEXT Web Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, NotRequired, TypedDict

from flext_cli import p, r, t, u

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

    @classmethod
    def create_application(
        cls,
        settings: FlextWebTypes.Web.ApplicationConfig,
    ) -> p.Result[m.Web.Entity]:
        """Create application model instance."""
        try:
            entity = m.Web.Entity(
                name=settings.name or "",
                host=settings.host or "localhost",
                port=settings.port or 8080,
                status=settings.status or c.Web.Status.STOPPED.value,
                environment=settings.environment or c.Web.Name.DEVELOPMENT.value,
                debug_mode=settings.debug_mode,
                version=settings.version,
                domain_events=[],
            )
            return r[m.Web.Entity].ok(entity)
        except c.EXC_BROAD_IO_TYPE as exc:
            return r[m.Web.Entity].fail(f"Failed to create application: {exc}")

    @classmethod
    def create_http_request(
        cls,
        url: str,
        method: str = c.Web.Method.GET,
        headers: t.StrMapping | None = None,
        body: str | t.MappingKV[str, t.Scalar] | None = None,
        timeout: float = c.Web.DEFAULT_TIMEOUT_SECONDS,
    ) -> p.Result[m.Web.Request]:
        """Create HTTP request model instance with proper validation."""
        method_upper = method.upper()
        valid_methods = set(c.Web.HTTP_METHODS)
        method_validated = u.guard(method_upper, str, return_value=True)
        if (
            not isinstance(method_validated, str)
            or method_validated not in valid_methods
        ):
            return r[m.Web.Request].fail(
                f"Invalid HTTP method: {method}. Must be one of: {valid_methods}",
            )
        try:
            request = m.Web.Request.model_validate({
                "url": url,
                "method": method_upper,
                "headers": dict(headers or {}),
                "body": body,
                "timeout": timeout,
            })
            return r[m.Web.Request].ok(request)
        except c.EXC_BROAD_IO_TYPE as exc:
            return r[m.Web.Request].fail(f"Failed to create HTTP request: {exc}")

    @classmethod
    def create_http_response(
        cls,
        status_code: int,
        headers: t.StrMapping | None = None,
        body: str | t.MappingKV[str, t.Scalar] | None = None,
        elapsed_time: float | None = None,
    ) -> p.Result[m.Web.Response]:
        """Create HTTP response model instance with proper validation."""
        try:
            response = m.Web.Response.model_validate({
                "status_code": status_code,
                "headers": dict(headers or {}),
                "body": body,
                "elapsed_time": elapsed_time,
            })
            return r[m.Web.Response].ok(response)
        except c.EXC_BROAD_IO_TYPE as exc:
            return r[m.Web.Response].fail(f"Failed to create HTTP response: {exc}")

    @classmethod
    def create_web_request(
        cls,
        settings: FlextWebTypes.Web.RequestConfig,
    ) -> p.Result[m.Web.AppRequest]:
        """Create web request model instance with proper validation."""
        if not settings.url or not settings.url.strip():
            return r[m.Web.AppRequest].fail("URL is required")
        method_upper = (settings.method or c.Web.Method.GET).upper()
        valid_methods = set(c.Web.HTTP_METHODS)
        method_validated = u.guard(method_upper, str, return_value=True)
        if (
            not isinstance(method_validated, str)
            or method_validated not in valid_methods
        ):
            return r[m.Web.AppRequest].fail(
                f"Invalid HTTP method: {settings.method}. "
                f"Must be one of: {valid_methods}",
            )
        try:
            request = m.Web.AppRequest.model_validate({
                "url": settings.url.strip(),
                "method": method_upper,
                "headers": dict(settings.headers or {}),
                "body": settings.body,
                "timeout": settings.timeout or c.Web.DEFAULT_TIMEOUT_SECONDS,
                "query_params": dict(settings.query_params or {}),
                "client_ip": settings.client_ip or "",
                "user_agent": settings.user_agent or "",
            })
            return r[m.Web.AppRequest].ok(request)
        except c.EXC_BROAD_IO_TYPE as exc:
            return r[m.Web.AppRequest].fail(f"Failed to create web request: {exc}")

    @classmethod
    def create_web_response(
        cls,
        settings: FlextWebTypes.Web.ResponseConfig,
    ) -> p.Result[m.Web.AppResponse]:
        """Create web response model instance with proper validation."""
        try:
            response = m.Web.AppResponse.model_validate({
                "status_code": settings.status_code or 200,
                "request_id": settings.request_id or "",
                "headers": dict(settings.headers or {}),
                "body": settings.body,
                "elapsed_time": settings.elapsed_time or 0.0,
                "content_type": (settings.content_type or c.Web.HTTP_CONTENT_TYPE_JSON),
                "content_length": settings.content_length or 0,
                "processing_time_ms": settings.processing_time_ms or 0.0,
            })
            return r[m.Web.AppResponse].ok(response)
        except c.EXC_BROAD_IO_TYPE as exc:
            return r[m.Web.AppResponse].fail(f"Failed to create web response: {exc}")


t = FlextWebTypes

__all__: list[str] = [
    "FlextWebTypes",
    "t",
]
