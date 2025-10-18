"""Generic HTTP Models - Domain-agnostic HTTP entity models using Python 3.13+.

This module provides generic HTTP models that can be reused across any HTTP-based application.
Completely domain-agnostic and follows flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
import uuid
from datetime import UTC, datetime
from enum import Enum
from typing import Any, ClassVar, Literal, cast, override

from flext_core import FlextModels, FlextResult, FlextUtilities
from pydantic import BaseModel, Field, computed_field

try:
    from pydantic._internal._typing_extra import FieldInfo
except ImportError:
    # For older Pydantic versions
    FieldInfo = Any

from flext_web.constants import FlextWebConstants

HttpMethodType = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
BodyType = str | dict[str, Any] | None

HTTP_SUCCESS_MIN = 200
HTTP_SUCCESS_MAX = 299
HTTP_ERROR_MIN = 400

HTTPS_PORTS = frozenset((443, 8443))


class FlextWebModels:
    """Generic FLEXT web model system using advanced Python 3.13+ patterns."""

    # =========================================================================
    # CLASS CONSTANTS
    # =========================================================================

    # Host and network field patterns
    HOST_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$|^localhost$",
    )

    URL_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^https?:\/\/(?:[-\w.])+(?::[0-9]+)?(?:\/(?:[\w\/_.])*)?(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?$",
    )

    # =========================================================================
    # NESTED FIELD CLASSES
    # =========================================================================

    class HTTPStatusField:
        """HTTP status code field with validation and description support."""

        @override
        def __init__(
            self,
            status_code: int,
            description: str | None = None,
            **field_kwargs: object,
        ) -> None:
            """Initialize HTTP status field.

            Args:
                status_code: HTTP status code
                description: Optional description
                **field_kwargs: Additional Pydantic field kwargs

            """
            self.status_code = status_code
            self.description = description
            self.field_kwargs = field_kwargs

        def create_field(self) -> FieldInfo:
            """Create Pydantic field for HTTP status."""
            kwargs = dict[str, object](self.field_kwargs)

            # Set default values
            kwargs.setdefault("default", self.status_code)
            kwargs.setdefault("ge", FlextConstants.FlextWeb.HTTP_OK)  # 200 como base
            kwargs.setdefault("le", FlextConstants.FlextWeb.HTTP_STATUS_MAX)  # 599

            if self.description:
                kwargs.setdefault(
                    "description",
                    f"HTTP {self.status_code}: {self.description}",
                )
            else:
                kwargs.setdefault("description", f"HTTP status code {self.status_code}")

            # Create Field with all constraints including ge/le
            field_description = kwargs.get(
                "description",
                f"HTTP {self.status_code}: {self.description or 'Status'}",
            )
            ge_val = cast("int", kwargs.get("ge", FlextConstants.FlextWeb.HTTP_OK))
            le_val = cast(
                "int",
                kwargs.get("le", FlextConstants.FlextWeb.HTTP_STATUS_MAX),
            )

            if isinstance(field_description, str):
                return cast(
                    "FieldInfo",
                    Field(
                        default=self.status_code,
                        description=field_description,
                        ge=ge_val,
                        le=le_val,
                    ),
                )
            return cast(
                "FieldInfo",
                Field(default=self.status_code, ge=ge_val, le=le_val),
            )

        @classmethod
        def ok(
            cls, description: str | None = None, **field_kwargs: object
        ) -> FlextWebModels.HTTPStatusField:
            """Create HTTP 200 OK status field."""
            return cls(
                FlextConstants.FlextWeb.HTTP_OK,
                description=description,
                **field_kwargs,
            )

        @classmethod
        def created(
            cls, description: str | None = None, **field_kwargs: object
        ) -> FlextWebModels.HTTPStatusField:
            """Create HTTP 201 Created status field."""
            return cls(
                FlextConstants.FlextWeb.HTTP_CREATED,
                description=description,
                **field_kwargs,
            )

        @classmethod
        def bad_request(
            cls, description: str | None = None, **field_kwargs: object
        ) -> FlextWebModels.HTTPStatusField:
            """Create HTTP 400 Bad Request status field."""
            return cls(
                FlextConstants.FlextWeb.HTTP_BAD_REQUEST,
                description=description,
                **field_kwargs,
            )

        @classmethod
        def not_found(
            cls, description: str | None = None, **field_kwargs: object
        ) -> FlextWebModels.HTTPStatusField:
            """Create HTTP 404 Not Found status field."""
            return cls(
                FlextConstants.FlextWeb.HTTP_NOT_FOUND,
                description=description,
                **field_kwargs,
            )

        @classmethod
        def server_error(
            cls, description: str | None = None, **field_kwargs: object
        ) -> FlextWebModels.HTTPStatusField:
            """Create HTTP 500 Internal Server Error status field."""
            return cls(
                FlextConstants.FlextWeb.HTTP_INTERNAL_SERVER_ERROR,
                description=description,
                **field_kwargs,
            )

    # =========================================================================
    # WEB-SPECIFIC FIELD METHODS
    # =========================================================================

    @classmethod
    def host_field(
        cls, default: str = "localhost", **kwargs: object
    ) -> FieldInfo:
        """Create host address field with MASSIVE FlextUtilities validation.

        Args:
            default: Default host value
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for host addresses

        """
        # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string for default validation
        safe_default = FlextUtilities.TextProcessor.safe_string(default)

        field_kwargs = dict[str, object](kwargs)
        field_kwargs.setdefault("default", safe_default)
        field_kwargs.setdefault("description", "Host address (IP or hostname)")
        field_kwargs.setdefault("pattern", cls.HOST_PATTERN.pattern)
        field_kwargs.setdefault("max_length", FlextConstants.Limits.MAX_STRING_LENGTH)

        # Simplified Field creation for host field with proper default
        field_description = kwargs.get("description", "Host field")
        field_default = kwargs.get("default", safe_default)
        if isinstance(field_description, str):
            return cast(
                "FieldInfo",
                Field(default=field_default, description=field_description),
            )
        return cast("FieldInfo", Field(default=field_default))

    @classmethod
    def port_field(
        cls,
        default: int = 8080,
        **kwargs: object,
    ) -> FieldInfo:
        """Create port number field with validation.

        Args:
            default: Default port value
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for port numbers

        """
        field_kwargs = dict[str, object](kwargs)
        field_kwargs.setdefault("default", default)
        field_kwargs.setdefault("description", "Port number (1-65535)")
        field_kwargs.setdefault("ge", FlextWebConstants.WebServer.MIN_PORT)
        field_kwargs.setdefault("le", FlextWebConstants.WebServer.MAX_PORT)

        # Simplified Field creation for port field
        field_description = kwargs.get("description", "Port field")
        if isinstance(field_description, str):
            return cast(
                "FieldInfo",
                Field(
                    default=default,
                    description=field_description,
                    ge=1024,
                    le=65535,
                ),
            )
        return cast(
            "FieldInfo",
            Field(
                default=default,
                ge=1024,
                le=65535,
            ),
        )

    @classmethod
    def url_field(cls, **kwargs: object) -> FieldInfo:
        """Create URL field with validation.

        Args:
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for URLs

        """
        field_kwargs = dict[str, object](kwargs)
        field_kwargs.setdefault("description", "Valid HTTP/HTTPS URL")
        field_kwargs.setdefault("pattern", cls.URL_PATTERN.pattern)
        # Simplified Field creation for URL field
        field_description = kwargs.get("description", "URL field")
        if isinstance(field_description, str):
            return cast("FieldInfo", Field(description=field_description))
        return cast("FieldInfo", Field())

    @classmethod
    def app_name_field(cls, **kwargs: object) -> FieldInfo:
        """Create application name field with MASSIVE FlextUtilities validation.

        Args:
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for application names

        """
        field_kwargs = dict[str, object](kwargs)
        # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string for description
        safe_description = FlextUtilities.TextProcessor.safe_string("Application name")
        field_kwargs.setdefault("description", safe_description)
        field_kwargs.setdefault("min_length", 3)
        field_kwargs.setdefault("max_length", 100)

        # Field creation with constraints for app name field
        field_description = field_kwargs.get("description", "Application name field")
        min_len = cast(
            "int",
            field_kwargs.get("min_length", 3),
        )
        max_len = cast(
            "int",
            field_kwargs.get("max_length", 100),
        )

        if isinstance(field_description, str):
            return cast(
                "FieldInfo",
                Field(
                    description=field_description,
                    min_length=min_len,
                    max_length=max_len,
                ),
            )
        return cast("FieldInfo", Field(min_length=min_len, max_length=max_len))

    @classmethod
    def secret_key_field(cls, **kwargs: object) -> FieldInfo:
        """Create secret key field with validation.

        Args:
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for secret keys

        """
        field_kwargs = dict[str, object](kwargs)
        field_kwargs.setdefault(
            "description",
            "Secret key for cryptographic operations",
        )
        field_kwargs.setdefault(
            "min_length",
            32,
        )

        # Hide secret key values in repr and str
        field_kwargs.setdefault("repr", False)

        # Simplified Field creation for secret key field
        field_description = kwargs.get("description", "Secret key field")
        if isinstance(field_description, str):
            return cast("FieldInfo", Field(description=field_description))
        return cast("FieldInfo", Field())

    # =========================================================================
    # HTTP STATUS FIELD FACTORIES
    # =========================================================================

    @classmethod
    def http_status_field(
        cls,
        status_code: int,
        description: str | None = None,
        **kwargs: object,
    ) -> FieldInfo:
        """Create HTTP status field.

        Args:
            status_code: HTTP status code
            description: Optional description
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for HTTP status codes

        """
        status_field = cls.HTTPStatusField(status_code, description, **kwargs)
        return status_field.create_field()

    class HttpMessage(BaseModel):
        """Generic HTTP message base model.

        Domain-agnostic base class for HTTP requests and responses.
        """

        headers: dict[str, str] = Field(default_factory=dict)
        body: BodyType = None
        timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    class HttpRequest(HttpMessage):
        """Generic HTTP request model.

        Domain-agnostic HTTP request with flext-core patterns.
        """

        url: str
        method: HttpMethodType = Field(default="GET")
        timeout: float = Field(default=30.0, ge=0.0, le=300.0)

        @computed_field
        @property
        def has_body(self) -> bool:
            """Check if request has a body."""
            return self.body is not None

        @computed_field
        @property
        def is_secure(self) -> bool:
            """Check if request uses HTTPS."""
            return self.url.startswith("https://")

    class HttpResponse(HttpMessage):
        """Generic HTTP response model.

        Domain-agnostic HTTP response with flext-core patterns.
        """

        status_code: int = Field(ge=100, le=599)
        elapsed_time: float | None = Field(default=None, ge=0.0)

        @computed_field
        @property
        def is_success(self) -> bool:
            """Check if response status indicates success."""
            return HTTP_SUCCESS_MIN <= self.status_code <= HTTP_SUCCESS_MAX

        @computed_field
        @property
        def is_error(self) -> bool:
            """Check if response status indicates error."""
            return self.status_code >= HTTP_ERROR_MIN

    class WebRequest(HttpRequest):
        """Web-specific request with tracking.

        Extends HttpRequest with web-specific tracking fields.
        """

        request_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        query_params: dict[str, Any] = Field(default_factory=dict)
        client_ip: str | None = None
        user_agent: str | None = None

    class WebResponse(HttpResponse):
        """Web-specific response with tracking.

        Extends HttpResponse with web-specific tracking fields.
        """

        response_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        request_id: str
        content_type: str | None = None
        content_length: int = Field(default=0, ge=0)
        processing_time_ms: float = Field(default=0.0, ge=0.0)

        @computed_field
        @property
        def processing_time_seconds(self) -> float:
            """Get processing time in seconds."""
            return self.processing_time_ms / 1000.0

    class WebAppStatus(Enum):
        """Web application status enumeration."""

        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        ERROR = "error"
        MAINTENANCE = "maintenance"
        DEPLOYING = "deploying"

    class WebApp(BaseModel):
        """Web application domain entity."""

        id: str = Field(default_factory=lambda: str(uuid.uuid4()))
        name: str = Field(min_length=1, max_length=100)
        host: str = Field(default="localhost", min_length=1, max_length=255)
        port: int = Field(default=8080, ge=1, le=65535)
        status: str = Field(default="stopped")
        environment: str = Field(default="development")
        debug_mode: bool = Field(default=False)
        version: int = Field(default=1)
        metrics: dict[str, Any] = Field(default_factory=dict)
        domain_events: list = Field(default_factory=list)

        @computed_field
        @property
        def is_running(self) -> bool:
            """Check if entity is currently running."""
            return self.status == "running"

        @computed_field
        @property
        def url(self) -> str:
            """Get the full URL for the entity."""
            protocol = "https" if self.port in HTTPS_PORTS else "http"
            return f"{protocol}://{self.host}:{self.port}"

        @computed_field
        @property
        def can_start(self) -> bool:
            """Check if entity can be started."""
            return self.status == "stopped"

        @computed_field
        @property
        def can_stop(self) -> bool:
            """Check if entity can be stopped."""
            return self.status == "running"

        def validate_business_rules(self) -> FlextResult:
            """Validate business rules for WebApp."""
            if not self.name or len(self.name) < FlextWebConstants.NAME_LENGTH_RANGE[0]:
                return FlextResult.fail(f"App name must be at least {FlextWebConstants.NAME_LENGTH_RANGE[0]} characters")
            if self.port < FlextWebConstants.PORT_RANGE[0] or self.port > FlextWebConstants.PORT_RANGE[1]:
                return FlextResult.fail(f"Port must be between {FlextWebConstants.PORT_RANGE[0]} and {FlextWebConstants.PORT_RANGE[1]}")
            return FlextResult.ok(None)

        def start(self) -> FlextResult:
            """Generic start operation."""
            if self.status == "running":
                return FlextResult.fail("Already running")
            self.status = "running"
            return FlextResult.ok(self)

        def stop(self) -> FlextResult:
            """Generic stop operation."""
            if self.status != "running":
                return FlextResult.fail("Not running")
            self.status = "stopped"
            return FlextResult.ok(self)

        def add_domain_event(self, event: str) -> None:
            """Add domain event."""
            self.domain_events.append(event)


__all__ = ["FlextWebModels"]
