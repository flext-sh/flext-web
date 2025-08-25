"""FLEXT Web Fields - Consolidated field system extending flext-core patterns.

This module implements the consolidated field architecture following the
"one class per module" pattern, with FlextWebFields extending FlextFields
and containing all web-specific field functionality as nested classes and methods.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Unpack, cast

from flext_core import FlextFields
from pydantic import Field
from pydantic.fields import FieldInfo

from flext_web.constants import FlextWebConstants
from flext_web.typings import FlextWebTypes

if TYPE_CHECKING:
    # For type checking, we can be more specific about return types
    FieldReturn = FieldInfo
else:
    FieldReturn = object


# =============================================================================
# CONSOLIDATED FIELDS CLASS
# =============================================================================


class FlextWebFields(FlextFields):
    """Consolidated web field system extending flext-core patterns.

    This class serves as the single point of access for all web-specific
    field definitions, validators, and serializers while extending FlextFields
    from flext-core for proper architectural inheritance.

    All field functionality is accessible through this single class following the
    "one class per module" architectural requirement.
    """

    # =========================================================================
    # CLASS CONSTANTS
    # =========================================================================

    # Host and network field patterns
    HOST_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$|^localhost$"
    )

    URL_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^https?:\/\/(?:[-\w.])+(?::[0-9]+)?(?:\/(?:[\w\/_.])*)?(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?$"
    )

    # =========================================================================
    # NESTED FIELD CLASSES
    # =========================================================================

    class HTTPStatusField:
        """HTTP status code field with validation and description support."""

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

        def create_field(self) -> FieldReturn:
            """Create Pydantic field for HTTP status."""
            kwargs = dict(self.field_kwargs)

            # Set default values
            kwargs.setdefault("default", self.status_code)
            kwargs.setdefault("ge", FlextWebConstants.HTTP.MIN_STATUS_CODE)
            kwargs.setdefault("le", FlextWebConstants.HTTP.MAX_STATUS_CODE)

            if self.description:
                kwargs.setdefault(
                    "description", f"HTTP {self.status_code}: {self.description}"
                )
            else:
                kwargs.setdefault("description", f"HTTP status code {self.status_code}")

            return cast("FieldInfo", Field(**kwargs))  # type: ignore[call-overload]

        @classmethod
        def ok(cls, **kwargs: object) -> HTTPStatusField:
            """Create HTTP 200 OK status field."""
            return cls(200, "OK", **kwargs)

        @classmethod
        def created(cls, **kwargs: object) -> HTTPStatusField:
            """Create HTTP 201 Created status field."""
            return cls(201, "Created", **kwargs)

        @classmethod
        def bad_request(cls, **kwargs: object) -> HTTPStatusField:
            """Create HTTP 400 Bad Request status field."""
            return cls(400, "Bad Request", **kwargs)

        @classmethod
        def not_found(cls, **kwargs: object) -> HTTPStatusField:
            """Create HTTP 404 Not Found status field."""
            return cls(404, "Not Found", **kwargs)

        @classmethod
        def server_error(cls, **kwargs: object) -> HTTPStatusField:
            """Create HTTP 500 Internal Server Error status field."""
            return cls(500, "Internal Server Error", **kwargs)

    # =========================================================================
    # WEB-SPECIFIC FIELD METHODS
    # =========================================================================

    @classmethod
    def host_field(cls, default: str = "localhost", **kwargs: object) -> FieldReturn:
        """Create host address field with validation.

        Args:
            default: Default host value
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for host addresses

        """
        field_kwargs = dict(kwargs)
        field_kwargs.setdefault("default", default)
        field_kwargs.setdefault("description", "Host address (IP or hostname)")
        field_kwargs.setdefault("pattern", cls.HOST_PATTERN.pattern)
        field_kwargs.setdefault(
            "max_length", FlextWebConstants.Validation.MAX_HOST_LENGTH
        )

        return cast("FieldReturn", Field(**field_kwargs))  # type: ignore[call-overload]

    @classmethod
    def port_field(
        cls,
        default: int = FlextWebConstants.Configuration.DEFAULT_PORT,
        **kwargs: object,
    ) -> FieldReturn:
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
        field_kwargs.setdefault("ge", FlextWebConstants.Network.MIN_PORT)
        field_kwargs.setdefault("le", FlextWebConstants.Network.MAX_PORT)

        return cast("FieldReturn", Field(**field_kwargs))  # type: ignore[call-overload]

    @classmethod
    def url_field(cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]) -> FieldReturn:
        """Create URL field with validation.

        Args:
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for URLs

        """
        field_kwargs = dict(kwargs)
        field_kwargs.setdefault("description", "Valid HTTP/HTTPS URL")
        field_kwargs.setdefault("pattern", cls.URL_PATTERN.pattern)

        return cast("FieldReturn", Field(**field_kwargs))  # type: ignore[call-overload]

    @classmethod
    def app_name_field(cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]) -> FieldReturn:
        """Create application name field with validation.

        Args:
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for application names

        """
        field_kwargs = dict(kwargs)
        field_kwargs.setdefault("description", "Application name")
        field_kwargs.setdefault(
            "min_length", FlextWebConstants.Validation.MIN_APP_NAME_LENGTH
        )
        field_kwargs.setdefault(
            "max_length", FlextWebConstants.Validation.MAX_APP_NAME_LENGTH
        )

        return cast("FieldReturn", Field(**field_kwargs))  # type: ignore[call-overload]

    @classmethod
    def secret_key_field(
        cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]
    ) -> FieldReturn:
        """Create secret key field with validation.

        Args:
            **kwargs: Additional Pydantic field kwargs

        Returns:
            Configured Pydantic field for secret keys

        """
        field_kwargs = dict(kwargs)
        field_kwargs.setdefault(
            "description", "Secret key for cryptographic operations"
        )
        field_kwargs.setdefault(
            "min_length", FlextWebConstants.Validation.MIN_SECRET_KEY_LENGTH
        )

        # Hide secret key values in repr and str
        field_kwargs.setdefault("repr", False)

        return cast("FieldReturn", Field(**field_kwargs))  # type: ignore[call-overload]

    # =========================================================================
    # HTTP STATUS FIELD FACTORIES
    # =========================================================================

    @classmethod
    def http_status_field(
        cls, status_code: int, description: str | None = None, **kwargs: object
    ) -> FieldReturn:
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

    @classmethod
    def ok_status_field(
        cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]
    ) -> FieldReturn:
        """Create HTTP 200 OK status field."""
        return cls.HTTPStatusField.ok(**kwargs).create_field()

    @classmethod
    def created_status_field(
        cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]
    ) -> FieldReturn:
        """Create HTTP 201 Created status field."""
        return cls.HTTPStatusField.created(**kwargs).create_field()

    @classmethod
    def bad_request_status_field(
        cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]
    ) -> FieldReturn:
        """Create HTTP 400 Bad Request status field."""
        return cls.HTTPStatusField.bad_request(**kwargs).create_field()

    @classmethod
    def not_found_status_field(
        cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]
    ) -> FieldReturn:
        """Create HTTP 404 Not Found status field."""
        return cls.HTTPStatusField.not_found(**kwargs).create_field()

    @classmethod
    def server_error_status_field(
        cls, **kwargs: Unpack[FlextWebTypes.FieldKwargs]
    ) -> FieldReturn:
        """Create HTTP 500 Internal Server Error status field."""
        return cls.HTTPStatusField.server_error(**kwargs).create_field()


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Legacy aliases for existing code compatibility
WebFields = FlextWebFields
HTTPStatusField = FlextWebFields.HTTPStatusField


__all__ = [
    "FlextWebFields",
    "HTTPStatusField",
    # Legacy compatibility exports
    "WebFields",
]
