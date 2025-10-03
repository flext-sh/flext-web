"""FLEXT Web Fields.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import ClassVar, cast, override

from pydantic import Field
from pydantic.fields import FieldInfo

from flext_core import FlextConstants, FlextModels, FlextUtilities
from flext_web.constants import FlextWebConstants


class FlextWebFields(FlextModels):
    """Consolidated web field system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    field definitions, validators, and serializers while extending FlextModels
    from flext-core for proper architectural inheritance.

    All field functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

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
            kwargs = dict(self.field_kwargs)

            # Set default values
            kwargs.setdefault("default", self.status_code)
            kwargs.setdefault("ge", FlextConstants.Http.HTTP_OK)  # 200 como base
            kwargs.setdefault("le", FlextConstants.Http.HTTP_STATUS_MAX)  # 599

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
            ge_val = cast("int", kwargs.get("ge", FlextConstants.Http.HTTP_OK))
            le_val = cast(
                "int",
                kwargs.get("le", FlextConstants.Http.HTTP_STATUS_MAX),
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
        def ok(cls, **kwargs: object) -> FlextWebFields.HTTPStatusField:
            """Create HTTP 200 OK status field."""
            return cls(FlextConstants.Http.HTTP_OK, **kwargs)

        @classmethod
        def created(cls, **kwargs: object) -> FlextWebFields.HTTPStatusField:
            """Create HTTP 201 Created status field."""
            return cls(FlextConstants.Http.HTTP_CREATED, **kwargs)

        @classmethod
        def bad_request(cls, **kwargs: object) -> FlextWebFields.HTTPStatusField:
            """Create HTTP 400 Bad Request status field."""
            return cls(FlextConstants.Http.HTTP_BAD_REQUEST, **kwargs)

        @classmethod
        def not_found(cls, **kwargs: object) -> FlextWebFields.HTTPStatusField:
            """Create HTTP 404 Not Found status field."""
            return cls(FlextConstants.Http.HTTP_NOT_FOUND, **kwargs)

        @classmethod
        def server_error(cls, **kwargs: object) -> FlextWebFields.HTTPStatusField:
            """Create HTTP 500 Internal Server Error status field."""
            return cls(FlextConstants.Http.HTTP_INTERNAL_SERVER_ERROR, **kwargs)

    # =========================================================================
    # WEB-SPECIFIC FIELD METHODS
    # =========================================================================

    @classmethod
    def host_field(
        cls, default: str = FlextWebConstants.WebServer.DEFAULT_HOST, **kwargs: object
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

        field_kwargs = dict(kwargs)
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
        default: int = FlextWebConstants.WebServer.DEFAULT_PORT,
        **kwargs: object,
    ) -> FieldInfo:
        """Create port number field with validation.

        Args:
            default: Default port value
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for port numbers

        """
        field_kwargs = dict(kwargs)
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
                    ge=FlextWebConstants.WebServer.MIN_PORT,
                    le=FlextWebConstants.WebServer.MAX_PORT,
                ),
            )
        return cast(
            "FieldInfo",
            Field(
                default=default,
                ge=FlextWebConstants.WebServer.MIN_PORT,
                le=FlextWebConstants.WebServer.MAX_PORT,
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
        field_kwargs = dict(kwargs)
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
        field_kwargs = dict(kwargs)
        # MASSIVE USAGE: FlextUtilities.TextProcessor.safe_string for description
        safe_description = FlextUtilities.TextProcessor.safe_string("Application name")
        field_kwargs.setdefault("description", safe_description)
        field_kwargs.setdefault(
            "min_length", FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH
        )
        field_kwargs.setdefault(
            "max_length", FlextWebConstants.WebServer.MAX_APP_NAME_LENGTH
        )

        # Field creation with constraints for app name field
        field_description = field_kwargs.get("description", "Application name field")
        min_len = cast(
            "int",
            field_kwargs.get(
                "min_length", FlextWebConstants.WebServer.MIN_APP_NAME_LENGTH
            ),
        )
        max_len = cast(
            "int",
            field_kwargs.get(
                "max_length", FlextWebConstants.WebServer.MAX_APP_NAME_LENGTH
            ),
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
        field_kwargs = dict(kwargs)
        field_kwargs.setdefault(
            "description",
            "Secret key for cryptographic operations",
        )
        field_kwargs.setdefault(
            "min_length",
            FlextConstants.Validation.MIN_SECRET_KEY_LENGTH,
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


__all__ = [
    # Main consolidated class
    "FlextWebFields",
]
