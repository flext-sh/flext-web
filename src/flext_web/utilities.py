"""FlextWeb-specific utilities extending flext-core patterns.

Minimal implementation providing ONLY web-domain-specific utilities not available
in flext-core. Delegates all generic operations to u.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import TYPE_CHECKING, override

from flext_cli import p, r, u

from flext_web import c, m

if TYPE_CHECKING:
    from flext_web import t


class FlextWebUtilities(u):
    """Web-specific utilities delegating to flext-core.

    Inherits from u and ensures consistency.
    Provides only web-domain-specific functionality not available in u.
    All generic operations delegate to flext-core utilities.
    Uses advanced builder/DSL patterns for composition.
    """

    class Web:
        """Web domain namespace."""

        RAISES: tuple[type[Exception], ...] = (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        )

        @staticmethod
        def create_application(
            settings: t.Web.ApplicationConfig,
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
            except FlextWebUtilities.Web.RAISES as exc:
                return r[m.Web.Entity].fail(f"Failed to create application: {exc}")

        @staticmethod
        def create_http_request(
            url: str,
            method: str = c.Web.Method.GET,
            headers: t.StrMapping | None = None,
            body: str | Mapping[str, t.Scalar] | None = None,
            timeout: float = c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
        ) -> p.Result[m.Web.Request]:
            """Create HTTP request model instance with proper validation."""
            method_upper = method.upper()
            valid_methods = set(c.Web.Http.METHODS)
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
            except FlextWebUtilities.Web.RAISES as exc:
                return r[m.Web.Request].fail(f"Failed to create HTTP request: {exc}")

        @staticmethod
        def create_http_response(
            status_code: int,
            headers: t.StrMapping | None = None,
            body: str | Mapping[str, t.Scalar] | None = None,
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
            except FlextWebUtilities.Web.RAISES as exc:
                return r[m.Web.Response].fail(f"Failed to create HTTP response: {exc}")

        @staticmethod
        def create_web_request(
            settings: t.Web.RequestConfig,
        ) -> p.Result[m.Web.AppRequest]:
            """Create web request model instance with proper validation."""
            if not settings.url or not settings.url.strip():
                return r[m.Web.AppRequest].fail("URL is required")
            method_upper = (settings.method or c.Web.Method.GET).upper()
            valid_methods = set(c.Web.Http.METHODS)
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
                    "timeout": settings.timeout or c.Web.Http.DEFAULT_TIMEOUT_SECONDS,
                    "query_params": dict(settings.query_params or {}),
                    "client_ip": settings.client_ip or "",
                    "user_agent": settings.user_agent or "",
                })
                return r[m.Web.AppRequest].ok(request)
            except FlextWebUtilities.Web.RAISES as exc:
                return r[m.Web.AppRequest].fail(f"Failed to create web request: {exc}")

        @staticmethod
        def create_web_response(
            settings: t.Web.ResponseConfig,
        ) -> p.Result[m.Web.AppResponse]:
            """Create web response model instance with proper validation."""
            try:
                response = m.Web.AppResponse.model_validate({
                    "status_code": settings.status_code or 200,
                    "request_id": settings.request_id or "",
                    "headers": dict(settings.headers or {}),
                    "body": settings.body,
                    "elapsed_time": settings.elapsed_time or 0.0,
                    "content_type": (
                        settings.content_type or c.Web.Http.CONTENT_TYPE_JSON
                    ),
                    "content_length": settings.content_length or 0,
                    "processing_time_ms": settings.processing_time_ms or 0.0,
                })
                return r[m.Web.AppResponse].ok(response)
            except FlextWebUtilities.Web.RAISES as exc:
                return r[m.Web.AppResponse].fail(
                    f"Failed to create web response: {exc}",
                )

    @staticmethod
    @override
    def format_app_id(name: str) -> str:
        """Format app name to valid ID using flext-core utilities.

        Uses proper validation and string operations.
        Fails fast if name is invalid (no fallbacks).

        Args:
            name: Application name to format

        Returns:
            Formatted application ID (prefixed with "app_")

        Raises:
            ValueError: If name cannot be formatted to valid ID

        """
        if not name:
            msg = f"Invalid application name: {name}"
            raise ValueError(msg)
        cleaned = FlextWebUtilities.safe_string(name)
        if not cleaned:
            msg = f"Application name cannot be empty: {name}"
            raise ValueError(msg)
        normalized_for_id = re.sub(r"[^\w\s-]+", "", cleaned)
        slug = FlextWebUtilities.slugify(normalized_for_id)
        if not slug:
            msg = f"Cannot format application name '{name}' to valid ID"
            raise ValueError(msg)
        return f"app_{slug}"

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-safe slug using standard string operations.

        Implements slugification without relying on non-existent DSL builders.
        """
        if not text:
            return ""
        normalized = text.lower()
        cleaned = re.sub(r"[^\w\s-]+", " ", normalized)
        words = re.split(r"[-\s]+", cleaned)
        truthy_words = [word for word in words if word]
        return "-".join(truthy_words)


u = FlextWebUtilities

__all__: list[str] = ["FlextWebUtilities", "u"]
