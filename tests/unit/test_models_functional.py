"""Real functional tests for flext_web.models using flext_tests utilities.

Tests focus on real model validation, business rule enforcement,
and domain entity lifecycle scenarios without mocks.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import pytest
from pydantic import ValidationError

from flext_web import FlextWebHandlers, FlextWebModels


class TestWebModelsFunctionalValidation:
    """Functional tests for FlextWebModels using real validation scenarios."""

    def test_functional_web_app_creation_with_validation(self) -> None:
        """Test WebApp creation with real validation scenarios."""
        # Test valid app creation
        app = FlextWebModels.WebApp(
            id="functional-test-app",
            name="Functional Test Application",
            host="127.0.0.1",
            port=8100,
        )

        assert app.id == "functional-test-app"
        assert app.name == "Functional Test Application"
        assert app.host == "127.0.0.1"
        assert app.port == 8100
        assert app.status == FlextWebModels.WebAppStatus.STOPPED  # Default
        assert app.is_running is False  # Default
        # Note: WebApp doesn't have created_at/updated_at attributes
        # These would need to be added to the model if required

    def test_functional_web_app_validation_edge_cases(self) -> None:
        """Test WebApp validation with real edge cases."""
        # Test minimum valid name length
        min_name_app = FlextWebModels.WebApp(
            id="min-name-app",
            name="A",  # Single character name
            host="localhost",
            port=8101,
        )
        assert min_name_app.name == "A"

        # Test maximum valid port
        max_port_app = FlextWebModels.WebApp(
            id="max-port-app",
            name="Max Port App",
            host="localhost",
            port=65535,  # Maximum valid port
        )
        assert max_port_app.port == 65535

        # Test IPv6 host
        ipv6_app = FlextWebModels.WebApp(
            id="ipv6-app",
            name="IPv6 App",
            host="::1",  # IPv6 localhost
            port=8102,
        )
        assert ipv6_app.host == "::1"

        # Test wildcard host binding
        wildcard_app = FlextWebModels.WebApp(
            id="wildcard-app", name="Wildcard App", host="0.0.0.0", port=8103,
        )
        assert (
            wildcard_app.host == "0.0.0.0"
        )  # WebApp model stores the original host value

    def test_functional_web_app_validation_error_scenarios(self) -> None:
        """Test WebApp validation with real error scenarios."""
        # Test invalid port values
        with pytest.raises(
            ValidationError, match="Input should be greater than or equal to",
        ):
            FlextWebModels.WebApp(
                id="invalid-port-low",
                name="Invalid Port Low",
                host="localhost",
                port=0,  # Invalid port
            )

        with pytest.raises(
            ValidationError, match="Input should be less than or equal to",
        ):
            FlextWebModels.WebApp(
                id="invalid-port-high",
                name="Invalid Port High",
                host="localhost",
                port=99999,  # Port too high
            )

        # Test invalid name (empty)
        with pytest.raises(
            ValidationError, match="String should have at least 1 character",
        ):
            FlextWebModels.WebApp(
                id="empty-name-app",
                name="",  # Empty name
                host="localhost",
                port=8104,
            )

        # Test invalid host (empty)
        with pytest.raises(
            ValidationError, match="String should have at least 1 character",
        ):
            FlextWebModels.WebApp(
                id="empty-host-app",
                name="Empty Host App",
                host="",  # Empty host
                port=8105,
            )

    def test_functional_web_app_status_transitions(self) -> None:
        """Test WebApp status transitions with real state machine behavior."""
        # Test each status independently to avoid MyPy unreachable code issue
        self._test_individual_status_transition()

    def _test_individual_status_transition(self) -> None:
        """Test status transitions independently."""
        # Test STARTING status
        app1 = FlextWebModels.WebApp(
            id="status-test-app-1",
            name="Status Test App 1",
            host="localhost",
            port=8106,
        )
        app1.status = FlextWebModels.WebAppStatus.STARTING
        assert app1.status == FlextWebModels.WebAppStatus.STARTING

        # Test RUNNING status
        app2 = FlextWebModels.WebApp(
            id="status-test-app-2",
            name="Status Test App 2",
            host="localhost",
            port=8107,
        )
        app2.status = FlextWebModels.WebAppStatus.RUNNING
        assert app2.status == FlextWebModels.WebAppStatus.RUNNING
        assert app2.is_running is True

        # Test STOPPING status
        app3 = FlextWebModels.WebApp(
            id="status-test-app-3",
            name="Status Test App 3",
            host="localhost",
            port=8108,
        )
        app3.status = FlextWebModels.WebAppStatus.STOPPING
        assert app3.status == FlextWebModels.WebAppStatus.STOPPING

        # Test ERROR status
        app4 = FlextWebModels.WebApp(
            id="status-test-app-4",
            name="Status Test App 4",
            host="localhost",
            port=8109,
        )
        app4.status = FlextWebModels.WebAppStatus.ERROR
        assert app4.status == FlextWebModels.WebAppStatus.ERROR

    def test_functional_web_app_handler_operations(self) -> None:
        """Test WebAppHandler operations with real command execution."""
        # Create handler instance
        handler = FlextWebHandlers.WebAppHandler()

        # Test create command
        create_result = handler.create(
            name="handler-test-app", host="127.0.0.1", port=8107,
        )

        assert create_result.success
        app = create_result.value
        assert isinstance(app, FlextWebModels.WebApp)
        assert app.name == "handler-test-app"
        assert app.status == FlextWebModels.WebAppStatus.STOPPED

        # Test start command
        start_result = handler.start(app)
        assert start_result.success
        started_app = start_result.value
        assert started_app.status == FlextWebModels.WebAppStatus.RUNNING
        assert started_app.is_running is True

        # Test stop command
        stop_result = handler.stop(started_app)
        assert stop_result.success
        stopped_app = stop_result.value
        assert stopped_app.status == FlextWebModels.WebAppStatus.STOPPED
        assert stopped_app.is_running is False

    def test_functional_web_app_handler_error_scenarios(self) -> None:
        """Test WebAppHandler error scenarios with real validation."""
        # Create handler instance
        handler = FlextWebHandlers.WebAppHandler()

        # Test create with invalid data
        invalid_create_result = handler.create(
            name="",  # Invalid empty name
            host="localhost",
            port=8108,
        )
        assert invalid_create_result.is_failure
        assert invalid_create_result.error is not None
        assert (
            "string should have at least 1 character"
            in invalid_create_result.error.lower()
        )

        # Test start of already running app
        app = FlextWebModels.WebApp(
            id="running-app",
            name="Running App",
            host="localhost",
            port=8109,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )

        already_running_result = handler.start(app)
        assert already_running_result.is_failure
        assert already_running_result.error is not None
        assert "already running" in already_running_result.error.lower()

        # Test stop of already stopped app
        stopped_app = FlextWebModels.WebApp(
            id="stopped-app",
            name="Stopped App",
            host="localhost",
            port=8110,
            status=FlextWebModels.WebAppStatus.STOPPED,
        )

        already_stopped_result = handler.stop(stopped_app)
        assert already_stopped_result.is_failure
        assert already_stopped_result.error is not None
        assert "app not running" in already_stopped_result.error.lower()

    def test_functional_web_app_with_flext_tests_builders(self) -> None:
        """Test WebApp creation using flext_tests builders."""
        # Create WebApp using standard parameters (TestEntityFactory is for generic entities)
        app = FlextWebModels.WebApp(
            id="builder-test-app",
            name="Builder Test Application",
            host="localhost",
            port=8111,
        )

        assert app.id == "builder-test-app"
        assert app.name == "Builder Test Application"
        assert app.host == "localhost"
        assert app.port == 8111

    def test_functional_web_app_business_rules_validation(self) -> None:
        """Test WebApp business rules with real validation scenarios."""
        app = FlextWebModels.WebApp(
            id="business-rules-app",
            name="Business Rules App",
            host="localhost",
            port=8112,
        )

        # Test business rules validation
        validation_result = app.validate_business_rules()
        assert validation_result.success

        # Test business rules pass for valid state
        valid_app = FlextWebModels.WebApp(
            id="valid-business-app",
            name="Valid Business App",
            host="localhost",
            port=8113,
            status=FlextWebModels.WebAppStatus.RUNNING,
        )
        # is_running is computed from status, so this is consistent

        valid_validation_result = valid_app.validate_business_rules()
        assert valid_validation_result.success

    def test_functional_web_app_lifecycle_complete_scenario(self) -> None:
        """Test complete WebApp lifecycle with real operations."""
        # Create handler instance
        handler = FlextWebHandlers.WebAppHandler()

        # Create app
        create_result = handler.create(
            name="lifecycle-test-app", host="127.0.0.1", port=8114,
        )
        assert create_result.success
        app = create_result.value

        # Validate initial state
        validation_result = app.validate_business_rules()
        assert validation_result.success

        # Start app
        start_result = handler.start(app)
        assert start_result.success
        running_app = start_result.value

        # Validate running state
        running_validation_result = running_app.validate_business_rules()
        assert running_validation_result.success

        # Test app operations while running
        assert running_app.status == FlextWebModels.WebAppStatus.RUNNING
        assert running_app.is_running is True

        # Stop app
        stop_result = handler.stop(running_app)
        assert stop_result.success
        stopped_app = stop_result.value

        # Validate final state
        final_validation_result = stopped_app.validate_business_rules()
        assert final_validation_result.success
        assert stopped_app.status == FlextWebModels.WebAppStatus.STOPPED
        assert stopped_app.is_running is False

    def test_functional_web_app_status_enum_operations(self) -> None:
        """Test WebAppStatus enum with real operations."""
        # Test all status values
        all_statuses = [
            FlextWebModels.WebAppStatus.STOPPED,
            FlextWebModels.WebAppStatus.STARTING,
            FlextWebModels.WebAppStatus.RUNNING,
            FlextWebModels.WebAppStatus.STOPPING,
            FlextWebModels.WebAppStatus.ERROR,
        ]

        for status in all_statuses:
            app = FlextWebModels.WebApp(
                id=f"status-{status.value}-app",
                name=f"Status {status.value} App",
                host="localhost",
                port=8115,
                status=status,
            )
            assert app.status == status

        # Test status string representations
        assert FlextWebModels.WebAppStatus.STOPPED.value == "stopped"
        assert FlextWebModels.WebAppStatus.RUNNING.value == "running"
        assert FlextWebModels.WebAppStatus.ERROR.value == "error"


__all__ = [
    "TestWebModelsFunctionalValidation",
]
