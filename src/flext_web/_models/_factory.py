"""Model factory methods for flext-web.

from flext_web import u
Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import uuid

from flext_cli import m, u

from flext_core import r
from flext_web import c, p, settings, t

from ._entity import FlextWebModelsEntity
from ._web_request import FlextWebModelsWebRequest


class FlextWebModelsFactory:
    """Factory methods for creating web models."""

    @classmethod
    def create_web_app(
        cls, name: str, host: str = settings.Web.host, port: int = settings.Web.port
    ) -> p.Result[FlextWebModelsEntity.Entity]:
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
        entity = FlextWebModelsEntity.Entity(
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
        return r[FlextWebModelsEntity.Entity].ok(entity)

    @classmethod
    def create_web_request(
        cls,
        method: c.Web.Method,
        url: str,
        headers: t.StrMapping | None = None,
        body: str | t.JsonValue | None = None,
    ) -> p.Result[FlextWebModelsWebRequest.WebRequest]:
        """Create a validated web request model from direct parameters."""
        payload: t.MutableMappingKV[str, t.JsonPayload] = {
            "method": method,
            "url": url,
            "headers": dict(headers or {}),
            "body": body,
            "request_id": str(uuid.uuid4()),
            "timestamp": u.now(),
        }
        return cls._build(FlextWebModelsWebRequest.WebRequest, payload, "web request")

    @classmethod
    def create_web_response(
        cls,
        request_id: str,
        status_code: int,
        headers: t.StrMapping | None = None,
        body: str | t.JsonValue | None = None,
    ) -> p.Result[FlextWebModelsWebRequest.WebResponse]:
        """Create a validated web response model from direct parameters."""
        payload: t.MutableMappingKV[str, t.JsonPayload] = {
            "request_id": request_id,
            "status_code": status_code,
            "headers": dict(headers or {}),
            "body": body,
            "response_id": str(uuid.uuid4()),
            "timestamp": u.now(),
        }
        return cls._build(FlextWebModelsWebRequest.WebResponse, payload, "web response")

    @staticmethod
    def _build[M: m.BaseModel](
        model_cls: type[M], payload: t.MutableMappingKV[str, t.JsonPayload], label: str
    ) -> p.Result[M]:
        """Validate a payload into ``model_cls`` at the Result boundary."""
        result = u.try_(lambda: model_cls.model_validate(payload), catch=Exception)
        return result.map_error(lambda exc: f"Failed to create {label}: {exc}")


__all__: list[str] = ["FlextWebModelsFactory"]
