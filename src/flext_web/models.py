"""FLEXT Web Models.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
import uuid
from enum import Enum

from flext_core import (
    FlextConstants,
    FlextMixins,
    FlextModels,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)
from pydantic import ConfigDict, Field, computed_field, field_validator

from flext_web.typings import FlextWebTypes


class FlextWebModels:
    """Consolidated FLEXT web model system with FlextMixins integration."""

    class WebAppStatus(Enum):
        """Web application status enumeration."""

        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"
        ERROR = "error"

    class WebApp(FlextModels.Entity):
        """Web application domain entity."""

        model_config = ConfigDict(
            validate_assignment=True,
            use_enum_values=True,
            extra="forbid",
            frozen=False,
        )

        name: str = Field(..., min_length=1, max_length=100)
        host: str = Field(default="localhost", min_length=1)
        port: int = Field(
            default=8080,
            ge=FlextConstants.Web.MIN_PORT,
            le=FlextConstants.Web.MAX_PORT,
        )
        status: FlextWebModels.WebAppStatus = Field(
            default_factory=lambda: FlextWebModels.WebAppStatus.STOPPED
        )

        @field_validator("status")
        @classmethod
        def validate_status(
            cls, v: FlextWebModels.WebAppStatus | str
        ) -> FlextWebModels.WebAppStatus:
            """Validate status field."""
            if isinstance(v, str):
                try:
                    return FlextWebModels.WebAppStatus(v)
                except ValueError as e:
                    msg = f"Invalid status: {v}"
                    raise ValueError(msg) from e
            return v

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate name field."""
            name = (v or "").strip()
            if not name:
                msg = "Name cannot be empty"
                raise ValueError(msg)

            reserved = {"REDACTED_LDAP_BIND_PASSWORD", "root", "api", "system"}
            if name.lower() in reserved:
                msg = f"Name '{name}' is reserved"
                raise ValueError(msg)

            dangerous = ["<", ">", "&", '"', "'", "script", "javascript"]
            if any(char in name.lower() for char in dangerous):
                msg = f"Name contains dangerous characters: {name}"
                raise ValueError(msg)

            return name

        @field_validator("host")
        @classmethod
        def validate_host(cls, v: str) -> str:
            """Validate host field with comprehensive format checking."""
            host = (v or "").strip()
            if not host:
                msg = "Host cannot be empty"
                raise ValueError(msg)

            # Use flext-core TextProcessor for safe string handling
            safe_host = FlextUtilities.TextProcessor.safe_string(host)
            if not safe_host:
                msg = f"Invalid host characters: {host}"
                raise ValueError(msg)

            safe_host = safe_host.strip()
            if not safe_host:
                msg = "Host cannot be empty after sanitization"
                raise ValueError(msg)

            # IPv4 pattern
            ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
            if re.match(ipv4_pattern, safe_host):
                return safe_host

            # Hostname pattern
            hostname_pattern = r"^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$"
            if re.match(hostname_pattern, safe_host):
                return safe_host

            # Special hostnames
            if safe_host.lower() in {"localhost", "127.0.0.1", "::", "::1"}:
                return safe_host

            msg = f"Invalid host format: {host}"
            raise ValueError(msg)

        @property
        def is_running(self) -> bool:
            """Check if app is running."""
            return self.status == FlextWebModels.WebAppStatus.RUNNING

        @property
        def url(self) -> str:
            """Get app URL."""
            # Standard HTTPS port is 443
            https_port = 443
            protocol = "https" if self.port == https_port else "http"
            return f"{protocol}://{self.host}:{self.port}"

        @computed_field
        def can_start(self) -> bool:
            """Check if app can be started."""
            return self.status == FlextWebModels.WebAppStatus.STOPPED

        @computed_field
        def can_stop(self) -> bool:
            """Check if app can be stopped."""
            return self.status == FlextWebModels.WebAppStatus.RUNNING

        def validate_business_rules(self) -> FlextResult[None]:
            """Validate business rules."""
            try:
                FlextMixins.initialize_validation(self)

                # Validate name field (same as field validator)
                name = (self.name or "").strip()
                if not name:
                    return FlextResult[None].fail("Application name is required")

                # Validate host field (same as field validator)
                host = (self.host or "").strip()
                if not host:
                    return FlextResult[None].fail("Host address is required")

                # Validate port range
                if not (
                    FlextConstants.Web.MIN_PORT
                    <= self.port
                    <= FlextConstants.Web.MAX_PORT
                ):
                    return FlextResult[None].fail(f"Port out of range: {self.port}")

                FlextMixins.log_operation(self, "validation_success")
                return FlextResult[None].ok(None)
            except Exception as e:
                return FlextResult[None].fail(f"Validation failed: {e}")

        def start(self) -> FlextResult[FlextWebModels.WebApp]:
            """Start application."""
            if self.status == FlextWebModels.WebAppStatus.RUNNING:
                return FlextResult[FlextWebModels.WebApp].fail("App already running")
            if self.status != FlextWebModels.WebAppStatus.STOPPED:
                return FlextResult[FlextWebModels.WebApp].fail("App not stopped")

            self.status = FlextWebModels.WebAppStatus.STARTING
            FlextMixins.update_timestamp(self)
            self.status = FlextWebModels.WebAppStatus.RUNNING
            FlextMixins.log_operation(self, "application_started")
            return FlextResult[FlextWebModels.WebApp].ok(self)

        def stop(self) -> FlextResult[FlextWebModels.WebApp]:
            """Stop application."""
            if self.status != FlextWebModels.WebAppStatus.RUNNING:
                return FlextResult[FlextWebModels.WebApp].fail("App not running")

            self.status = FlextWebModels.WebAppStatus.STOPPING
            FlextMixins.update_timestamp(self)
            self.status = FlextWebModels.WebAppStatus.STOPPED
            FlextMixins.log_operation(self, "application_stopped")
            return FlextResult[FlextWebModels.WebApp].ok(self)

        def to_dict(self) -> FlextTypes.Core.Dict:
            """Convert to dict."""
            return FlextMixins.to_dict(self)

        def __str__(self) -> str:
            """String representation of the WebApp."""
            return f"{self.name} ({self.host}:{self.port})"

        def __repr__(self) -> str:
            """Detailed string representation."""
            return f"WebApp(id='{self.id}', name='{self.name}', host='{self.host}', port={self.port}, status='{self.status.value}')"

        def model_post_init(self, __context: object, /) -> None:
            """Post-init setup."""
            super().model_post_init(__context)
            FlextMixins.create_timestamp_fields(self)
            FlextMixins.ensure_id(self)
            FlextMixins.initialize_validation(self)
            FlextMixins.log_operation(self, "webapp_created")

    @classmethod
    def create_web_app(
        cls, data: FlextWebTypes.AppData
    ) -> FlextResult[FlextWebModels.WebApp]:
        """Create web application."""
        try:
            app_data = dict(data)

            # Ensure ID
            if "id" not in app_data:
                app_data["id"] = f"app_{uuid.uuid4().hex[:8]}"

            # Ensure status
            if "status" not in app_data:
                app_data["status"] = FlextWebModels.WebAppStatus.STOPPED

            # Validate port type
            port = app_data["port"]
            if isinstance(port, str) and port.isdigit():
                app_data["port"] = int(port)
            elif not isinstance(port, int):
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Invalid port type: {type(port)}"
                )

            # Create app with explicit parameters to avoid type issues
            # Port is already validated to be int above
            port_value = app_data["port"]
            if not isinstance(port_value, int):
                return FlextResult[FlextWebModels.WebApp].fail(
                    f"Port validation failed: expected int, got {type(port_value)}"
                )

            app = FlextWebModels.WebApp(
                id=str(app_data["id"]),
                name=str(app_data["name"]),
                host=str(app_data["host"]),
                port=port_value,
                status=FlextWebModels.WebAppStatus(app_data["status"]),
            )

            validation_result = app.validate_business_rules()
            if validation_result.is_failure:
                return FlextResult[FlextWebModels.WebApp].fail(
                    validation_result.error or "Validation failed"
                )

            return FlextResult[FlextWebModels.WebApp].ok(app)

        except Exception as e:
            return FlextResult[FlextWebModels.WebApp].fail(f"App creation failed: {e}")


__all__ = ["FlextWebModels"]
