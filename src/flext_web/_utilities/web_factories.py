"""Web factory helpers — model construction with validation.

Private mixin composed into ``FlextWebUtilities`` via MRO. Hosts the
runtime model factories that previously lived in ``typings.py`` (a §2.2
violation: typings must be type aliases only).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING

from flext_cli import p, r, u

from flext_web import c, m

if TYPE_CHECKING:
    from flext_web import t


class FlextWebUtilitiesFactories:
    """Web model factory helpers; composed into ``u.Web`` via MRO."""

    class Web:
        """Web factory namespace (composed into FlextWebUtilities.Web)."""

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
            except FlextWebUtilitiesFactories.Web.RAISES as exc:
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
            except FlextWebUtilitiesFactories.Web.RAISES as exc:
                return r[m.Web.Request].fail(
                    f"Failed to create HTTP request: {exc}",
                )

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
            except FlextWebUtilitiesFactories.Web.RAISES as exc:
                return r[m.Web.Response].fail(
                    f"Failed to create HTTP response: {exc}",
                )

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
            except FlextWebUtilitiesFactories.Web.RAISES as exc:
                return r[m.Web.AppRequest].fail(
                    f"Failed to create web request: {exc}",
                )

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
            except FlextWebUtilitiesFactories.Web.RAISES as exc:
                return r[m.Web.AppResponse].fail(
                    f"Failed to create web response: {exc}",
                )


__all__: list[str] = ["FlextWebUtilitiesFactories"]
