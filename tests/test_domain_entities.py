"""FLEXT Web Interface - Domain Entity Testing Suite.

Enterprise-grade test suite for domain entities, business logic validation,
and state management patterns. Ensures domain models follow Domain-Driven Design
principles with proper business rule enforcement and state machine validation.

Test Coverage:
    - FlextWebApp entity lifecycle management and state transitions
    - FlextWebAppStatus enumeration and business rules
    - FlextWebAppHandler CQRS command processing
    - Domain validation and error handling patterns
    - Business logic consistency and rule enforcement

Integration:
    - Tests flext-core entity patterns and validation
    - Validates FlextResult railway-oriented programming
    - Ensures domain-driven design principles
    - Verifies Clean Architecture boundaries

Author: FLEXT Development Team
Version: 0.9.0
Status: Enterprise domain testing with comprehensive business logic coverage
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_web import FlextWebApp, FlextWebAppHandler, FlextWebAppStatus

# Constants
EXPECTED_TOTAL_PAGES = 8


class TestFlextWebApp:
    """Enterprise domain entity testing for FlextWebApp lifecycle management.

    Comprehensive test suite covering FlextWebApp domain entity creation,
    validation, state transitions, and business rule enforcement. Ensures
    domain-driven design principles and Clean Architecture boundaries.
    """

    def test_flext_web_app_creation(self) -> None:
      """Test FlextWebApp entity creation with comprehensive validation.

      Validates that FlextWebApp domain entity creates successfully with
      proper default values, business rule enforcement, and state initialization.
      Tests fundamental domain patterns used throughout the system.
      """
      app = FlextWebApp(id="app_test-app", name="TestApp", port=8080)

      if app.id != "app_test-app":
          msg: str = f"Expected {'app_test-app'}, got {app.id}"
          raise AssertionError(msg)
      assert app.name == "TestApp"
      if app.port != 8080:
          msg: str = f"Expected {8080}, got {app.port}"
          raise AssertionError(msg)
      assert app.host == "localhost"
      assert not app.is_running

    def test_webapp_validation(self) -> None:
      """Test FlextWebApp domain validation with business rules.

      Validates that FlextWebApp correctly enforces domain validation rules
      and returns proper FlextResult success/failure patterns.
      """
      app = FlextWebApp(id="app_test-app", name="TestApp", port=8080)
      result = app.validate_domain_rules()

      assert result.success

    def test_webapp_invalid_port(self) -> None:
      """Test FlextWebApp with invalid port validation."""
      with pytest.raises(ValidationError):
          FlextWebApp(id="app_test-app", name="TestApp", port=99999)

    def test_webapp_empty_name(self) -> None:
      """Test FlextWebApp domain validation with empty name."""
      app = FlextWebApp(id="app_test-app", name="", port=8080)
      result = app.validate_domain_rules()

      assert not result.success
      if "App name is required" not in result.error:
          msg: str = f"Expected {'App name is required'} in {result.error}"
          raise AssertionError(msg)

    def test_webapp_start(self) -> None:
      """Test FlextWebApp start operation with state transition."""
      app = FlextWebApp(id="app_test-app", name="TestApp", port=8080)
      result = app.start()

      assert result.success
      started_app = result.data
      assert started_app is not None
      assert started_app.is_running

    def test_webapp_stop(self) -> None:
      """Test FlextWebApp stop."""
      app = FlextWebApp(
          id="app_test-app",
          name="TestApp",
          port=8080,
          status=FlextWebAppStatus.RUNNING,
      )
      result = app.stop()

      assert result.success
      stopped_app = result.data
      assert stopped_app is not None
      assert not stopped_app.is_running


class TestFlextWebAppHandler:
    """Test FlextWebAppHandler."""

    def test_handler_create(self) -> None:
      """Test handler create."""
      handler = FlextWebAppHandler()
      result = handler.create("TestApp", port=8080)

      assert result.success
      app = result.data
      assert app is not None
      if app.name != "TestApp":
          msg: str = f"Expected {'TestApp'}, got {app.name}"
          raise AssertionError(msg)
      assert app.port == 8080

    def test_handler_start(self) -> None:
      """Test handler start."""
      handler = FlextWebAppHandler()
      app = FlextWebApp(id="app_test-app", name="TestApp", port=8080)

      result = handler.start(app)

      assert result.success
      started_app = result.data
      assert started_app is not None
      assert started_app.is_running

    def test_handler_stop(self) -> None:
      """Test handler stop."""
      handler = FlextWebAppHandler()
      app = FlextWebApp(
          id="app_test-app",
          name="TestApp",
          port=8080,
          status=FlextWebAppStatus.RUNNING,
      )

      result = handler.stop(app)

      assert result.success
      stopped_app = result.data
      assert stopped_app is not None
      assert not stopped_app.is_running
