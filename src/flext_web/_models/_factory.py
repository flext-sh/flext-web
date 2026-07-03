"""Model factory methods for flext-web.

from flext_web.utilities import u
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid

from flext_cli import p, r, t, u
from flext_web.constants import c

from ._entity import FlextWebModelsEntity
from ._web_request import FlextWebModelsWebRequest


class FlextWebModelsFactory:
    """Web model factory methods namespace."""

    class Web:
        """Factory methods for creating web models."""

        @classmethod
        def create_web_app(
            cls,
            name: str,
            host: str = c.Web.DEFAULT_HOST,
            port: int = c.Web.DEFAULT_PORT,
        ) -> p.Result[FlextWebModelsEntity.Web.Entity]:
            """Create a web application from direct parameters.

            No dict conversion - use direct parameters for type safety.
            Pydantic validation will handle errors automatically.

            Args:
                name: Application name
                host: Application host
                port: Application port

            Returns:
                r[Web.Entity]: Success contains entity,
                                            failure contains validation error

            """
            entity = FlextWebModelsEntity.Web.Entity(
                id=str(uuid.uuid4()),
                name=name,
                host=host,
                port=port,
                status=c.Web.Status.STOPPED.value,
                environment=c.Web.Name.DEVELOPMENT.value,
                debug_mode=False,
                metrics={},
                web_events=[],
            )
            return r[FlextWebModelsEntity.Web.Entity].ok(entity)

        @classmethod
        def create_web_request(
            cls,
            method: c.Web.Method,
            url: str,
            headers: t.StrMapping | None = None,
            body: str | t.JsonValue | None = None,
        ) -> p.Result[FlextWebModelsWebRequest.Web.WebRequest]:
            """Create a web request model.

            Args:
                method: HTTP method
                url: Request URL
                headers: Request headers (defaults to empty dict)
                body: Request body

            Returns:
                r[WebRequest]: Success contains request model,
                                        failure contains validation error

            """
            headers_validated: t.StrMapping = headers or {}

            def create_request() -> FlextWebModelsWebRequest.Web.WebRequest:
                """Create request model."""
                validated: FlextWebModelsWebRequest.Web.WebRequest = (
                    FlextWebModelsWebRequest.Web.WebRequest.model_validate({
                        "method": method,
                        "url": url,
                        "headers": dict(headers_validated),
                        "body": body,
                        "request_id": str(uuid.uuid4()),
                        "timestamp": u.now(),
                    })
                )
                return validated

            result = u.try_(
                create_request,
                catch=Exception,
            )
            return result.map_error(lambda exc: f"Failed to create web request: {exc}")

        @classmethod
        def create_web_response(
            cls,
            request_id: str,
            status_code: int,
            headers: t.StrMapping | None = None,
            body: str | t.JsonValue | None = None,
        ) -> p.Result[FlextWebModelsWebRequest.Web.WebResponse]:
            """Create a web response model.

            Args:
                request_id: Associated request identifier
                status_code: HTTP status code
                headers: Response headers (defaults to empty dict)
                body: Response body

            Returns:
                 r[WebResponse]: Success contains response model,
                                          failure contains validation error

            """
            headers_validated: t.StrMapping = headers or {}

            def create_response() -> FlextWebModelsWebRequest.Web.WebResponse:
                """Create response model."""
                validated: FlextWebModelsWebRequest.Web.WebResponse = (
                    FlextWebModelsWebRequest.Web.WebResponse.model_validate({
                        "request_id": request_id,
                        "status_code": status_code,
                        "headers": dict(headers_validated),
                        "body": body,
                        "response_id": str(uuid.uuid4()),
                        "timestamp": u.now(),
                    })
                )
                return validated

            result = u.try_(
                create_response,
                catch=Exception,
            )
            return result.map_error(lambda exc: f"Failed to create web response: {exc}")


__all__: list[str] = ["FlextWebModelsFactory"]
