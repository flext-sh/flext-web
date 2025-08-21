"""FLEXT Web Fields - Pydantic field definitions and validators for web domain.

This module provides specialized field definitions, validators, and
serializers for web-specific data types, extending the base field
patterns from flext-core.

Fields follow Pydantic v2 patterns with comprehensive validation,
serialization, and type safety for web domain models.

Key Components:
    - Web-specific field types
    - Custom validators for web data
    - Serialization helpers
    - Integration with HTTP request/response cycles
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, ClassVar, Unpack, cast

from flext_core import FlextFields
from pydantic import Field
from pydantic.fields import FieldInfo

from flext_web.constants import FlextWebConstants
from flext_web.type_aliases import (
    FieldKwargs,
    SchemaDict,
    ValidatorGenerator,
)

if TYPE_CHECKING:
    # For type checking, we can be more specific about return types
    FieldReturn = FieldInfo
else:
    FieldReturn = object


class WebFields(FlextFields):
    """Web-specific field definitions extending flext-core patterns.

    Provides specialized field types and validators for web domain
    models with HTTP-specific validation and serialization requirements.
    """

    # Host and network field patterns
    HOST_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$|^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$|^localhost$"
    )

    # URL pattern for validation
    URL_PATTERN: ClassVar[re.Pattern[str]] = re.compile(
        r"^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*)?(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?$"
    )

    @classmethod
    def app_name_field(cls, **kwargs: Unpack[FieldKwargs]) -> FieldReturn:
        """Create application name field with validation.

        Args:
            **kwargs: Field arguments including description, min_length, max_length

        Returns:
            Pydantic FieldInfo with app name validation.

        """
        field_kwargs = cast(
            "dict[str, object]",
            {
                "description": "Application name",
                "min_length": 1,
                "max_length": 255,
                **kwargs,
            },
        )
        return Field(**field_kwargs)

    @classmethod
    def host_field(cls, **kwargs: Unpack[FieldKwargs]) -> FieldReturn:
        """Create host field with validation.

        Args:
            **kwargs: Field arguments including description, default

        Returns:
            Pydantic FieldInfo with host validation.

        """
        field_kwargs = cast(
            "dict[str, object]",
            {"default": "localhost", "description": "Host address", **kwargs},
        )
        return Field(**field_kwargs)

    @classmethod
    def port_field(cls, **kwargs: Unpack[FieldKwargs]) -> FieldReturn:
        """Create port field with validation.

        Args:
            **kwargs: Field arguments including description, default

        Returns:
            Pydantic FieldInfo with port validation.

        """
        field_kwargs = cast(
            "dict[str, object]",
            {
                "default": 8000,
                "ge": 1,
                "le": 65535,
                "description": "Port number",
                **kwargs,
            },
        )
        return Field(**field_kwargs)

    @classmethod
    def url_field(cls, **kwargs: Unpack[FieldKwargs]) -> FieldReturn:
        """Create URL field with validation.

        Args:
            **kwargs: Field arguments including description

        Returns:
            Pydantic FieldInfo with URL validation.

        """
        field_kwargs = cast(
            "dict[str, object]", {"description": "URL address", **kwargs}
        )
        return Field(**field_kwargs)

    @classmethod
    def secret_key_field(cls, **kwargs: Unpack[FieldKwargs]) -> FieldReturn:
        """Create secret key field with validation.

        Args:
            **kwargs: Field arguments including description, min_length

        Returns:
            Pydantic FieldInfo with secret key validation.

        """
        field_kwargs = cast(
            "dict[str, object]",
            {"description": "Cryptographic secret key", "min_length": 32, **kwargs},
        )
        return Field(**field_kwargs)

    @staticmethod
    def validate_app_name(value: str) -> str:
        """Validate application name format.

        Args:
            value: Application name to validate

        Returns:
            Validated application name.

        Raises:
            ValueError: If name format is invalid.

        """
        if not value:
            msg = "Application name cannot be empty"
            raise ValueError(msg)

        if not re.match(r"^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$", value):
            msg = (
                "Application name must start and end with alphanumeric characters "
                "and contain only letters, numbers, hyphens, and underscores"
            )
            raise ValueError(msg)

        if len(value) > FlextWebConstants.Validation.MAX_APP_NAME_LENGTH:
            msg = f"Application name must be {FlextWebConstants.Validation.MAX_APP_NAME_LENGTH} characters or less"
            raise ValueError(msg)

        return value

    @staticmethod
    def validate_host(value: str) -> str:
        """Validate host address format.

        Args:
            value: Host address to validate

        Returns:
            Validated host address.

        Raises:
            ValueError: If host format is invalid.

        """
        if not value:
            msg = "Host address cannot be empty"
            raise ValueError(msg)

        if not WebFields.HOST_PATTERN.match(value):
            msg = "Host must be a valid IP address, domain name, or 'localhost'"
            raise ValueError(msg)

        return value

    @staticmethod
    def validate_port(value: int) -> int:
        """Validate port number range.

        Args:
            value: Port number to validate

        Returns:
            Validated port number.

        Raises:
            ValueError: If port is out of valid range.

        """
        min_port = FlextWebConstants.Network.MIN_PORT
        max_port = FlextWebConstants.Network.MAX_PORT
        if not (min_port <= value <= max_port):
            msg = f"Port must be between {min_port} and {max_port}"
            raise ValueError(msg)

        return value

    @staticmethod
    def validate_url(value: str) -> str:
        """Validate URL format.

        Args:
            value: URL to validate

        Returns:
            Validated URL.

        Raises:
            ValueError: If URL format is invalid.

        """
        if not value:
            msg = "URL cannot be empty"
            raise ValueError(msg)

        if not WebFields.URL_PATTERN.match(value):
            msg = "URL must be a valid HTTP or HTTPS URL"
            raise ValueError(msg)

        return value

    @staticmethod
    def validate_secret_key(value: str) -> str:
        """Validate secret key strength.

        Args:
            value: Secret key to validate

        Returns:
            Validated secret key.

        Raises:
            ValueError: If secret key is weak or invalid.

        """
        if not value:
            msg = "Secret key cannot be empty"
            raise ValueError(msg)

        min_length = FlextWebConstants.Validation.MIN_SECRET_KEY_LENGTH
        if len(value) < min_length:
            msg = f"Secret key must be at least {min_length} characters long"
            raise ValueError(msg)

        if value == "development-secret-change-in-production":
            msg = "Default development secret key must be changed in production"
            raise ValueError(msg)

        return value


class HTTPStatusField:
    """HTTP status code field with validation."""

    @staticmethod
    def __get_validators__() -> ValidatorGenerator:
        """Get Pydantic validators."""
        yield HTTPStatusField.validate

    @staticmethod
    def validate(value: object) -> int:
        """Validate HTTP status code.

        Args:
            value: Status code to validate

        Returns:
            Validated status code.

        Raises:
            ValueError: If status code is invalid.

        """
        if not isinstance(value, int):
            msg = "Status code must be an integer"
            raise TypeError(msg)

        min_status = FlextWebConstants.HTTP.MIN_STATUS_CODE
        max_status = FlextWebConstants.HTTP.MAX_STATUS_CODE
        if not (min_status <= value <= max_status):
            msg = f"Status code must be between {min_status} and {max_status}"
            raise ValueError(msg)

        return value

    @staticmethod
    def __modify_schema__(field_schema: SchemaDict) -> None:
        """Modify Pydantic schema for documentation."""
        field_schema.update(
            type="integer", minimum=100, maximum=599, description="HTTP status code"
        )
