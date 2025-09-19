"""FLEXT Web Interface - Domain Entity Testing Suite.

Enterprise-grade test suite for domain entities, business logic validation,
and state management patterns. Ensures domain models follow Domain-Driven Design
principles with proper business rule enforcement and state machine validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_web import (
    FlextWebHandlers,
    FlextWebModels,
)


class TestWebApp:
    """Enterprise domain entity testing for FlextWebModels.WebApp lifecycle management.

    Comprehensive test suite covering FlextWebModels.WebApp domain entity creation,
    validation, state transitions, and business rule enforcement. Ensures
    domain-driven design principles and Clean Architecture boundaries.
    """

    def test_flext_web_app_creation(self) -> None:
        """Test FlextWebModels.WebApp entity creation with comprehensive validation.

        Validates that FlextWebModels.WebApp domain entity creates successfully with
        proper default values, business rule enforcement, and state initialization.
        Tests fundamental domain patterns used throughout the system.
        """
        app = FlextWebModels.WebApp(id="app_test-app", name="TestApp", port=8080)

        if app.id != "app_test-app":
            msg: str = f"Expected {'app_test-app'}, got {app.id}"
            raise AssertionError(msg)
        assert app.name == "TestApp"
        if app.port != 8080:
            port_msg: str = f"Expected {8080}, got {app.port}"
            raise AssertionError(port_msg)
        assert app.host == "localhost"
        assert not app.is_running

    def test_webapp_validation(self) -> None:
        """Test FlextWebModels.WebApp domain validation with business rules.

        Validates that FlextWebModels.WebApp correctly enforces domain validation rules
        and returns proper FlextResult success/failure patterns.
        """
        app = FlextWebModels.WebApp(id="app_test-app", name="TestApp", port=8080)
        result = app.validate_business_rules()

        assert result.is_success

    def test_webapp_invalid_port(self) -> None:
        """Test FlextWebModels.WebApp with invalid port validation."""
        with pytest.raises(ValidationError):
            FlextWebModels.WebApp(id="app_test-app", name="TestApp", port=99999)

    def test_webapp_empty_name(self) -> None:
        """Test FlextWebModels.WebApp domain validation with empty name."""
        # Empty name should fail at construction time with Pydantic validation
        with pytest.raises(
            ValidationError, match="String should have at least 1 character",
        ):
            FlextWebModels.WebApp(id="app_test-app", name="", port=8080)

    def test_webapp_start(self) -> None:
        """Test FlextWebModels.WebApp start operation with state transition."""
        app = FlextWebModels.WebApp(id="app_test-app", name="TestApp", port=8080)
        result = app.start()

        assert result.success
        started_app = result.value
        assert started_app is not None
        assert started_app.is_running

    def test_webapp_stop(self) -> None:
        """Test FlextWebModels.WebApp stop."""
        app = FlextWebModels.WebApp(
            id="app_test-app",
            name="TestApp",
            port=8080,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )
        result = app.stop()

        assert result.success
        stopped_app = result.value
        assert stopped_app is not None
        assert not stopped_app.is_running


class TestWebAppHandler:
    """Test FlextWebModels.WebAppHandler."""

    def test_handler_create(self) -> None:
        """Test handler create."""
        handler = FlextWebHandlers.WebAppHandler()
        result = handler.create("TestApp", port=8080)

        assert result.success
        app = result.value
        assert app is not None
        if app.name != "TestApp":
            msg: str = f"Expected {'TestApp'}, got {app.name}"
            raise AssertionError(msg)
        assert app.port == 8080

    def test_handler_start(self) -> None:
        """Test handler start."""
        handler = FlextWebHandlers.WebAppHandler()
        app = FlextWebModels.WebApp(id="app_test-app", name="TestApp", port=8080)

        result = handler.start(app)

        assert result.success
        started_app = result.value
        assert started_app is not None
        assert started_app.is_running

    def test_handler_stop(self) -> None:
        """Test handler stop."""
        handler = FlextWebHandlers.WebAppHandler()
        app = FlextWebModels.WebApp(
            id="app_test-app",
            name="TestApp",
            port=8080,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )

        result = handler.stop(app)

        assert result.success
        stopped_app = result.value
        assert stopped_app is not None
        assert not stopped_app.is_running
