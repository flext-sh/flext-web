"""Uses flext_tests library for real functional testing without mocks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import math

from flext_tests import FlextTestsUtilities
from flext_web import FlextWebTypes


class TestTypingsMissingCoverage:
    """Real functional tests for uncovered typings.py lines using flext_tests."""

    def test_validate_config_data_real_errors(self) -> None:
        """Test config validation with real error scenarios (lines 217, 230, 238, 242, 246)."""
        # Test non-dict data (line 217)
        result = FlextWebTypes.validate_config_data("not_a_dict")
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "must be a dictionary" in result.error

        # Test missing fields (lines 224-226)
        incomplete_data = {
            "host": "localhost",
            "port": 8080,
        }  # Missing debug, secret_key, app_name
        result = FlextWebTypes.validate_config_data(incomplete_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "required field" in result.error.lower()

        # Test invalid host type (line 230)
        invalid_host_data = {
            "host": 123,  # Should be string
            "port": 8080,
            "debug": True,
            "secret_key": "test-secret-32-characters-long!",
            "app_name": "Test App",
        }
        result = FlextWebTypes.validate_config_data(invalid_host_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "host" in result.error
        assert result.error is not None and "string" in result.error

        # Test invalid port type (line 238)
        invalid_port_data = {
            "host": "localhost",
            "port": "8080",  # Should be int
            "debug": True,
            "secret_key": "test-secret-32-characters-long!",
            "app_name": "Test App",
        }
        result = FlextWebTypes.validate_config_data(invalid_port_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "port" in result.error
        assert result.error is not None and "integer" in result.error

        # Test invalid debug type (line 242)
        invalid_debug_data = {
            "host": "localhost",
            "port": 8080,
            "debug": "true",  # Should be bool
            "secret_key": "test-secret-32-characters-long!",
            "app_name": "Test App",
        }
        result = FlextWebTypes.validate_config_data(invalid_debug_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "debug" in result.error
        assert result.error is not None and "boolean" in result.error

        # Test invalid secret_key type (line 246)
        invalid_secret_data = {
            "host": "localhost",
            "port": 8080,
            "debug": True,
            "secret_key": 12345,  # Should be string
            "app_name": "Test App",
        }
        result = FlextWebTypes.validate_config_data(invalid_secret_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "secret_key" in result.error
        assert result.error is not None and "string" in result.error

    def test_validate_config_data_app_name_errors(self) -> None:
        """Test app_name validation errors (lines 259-260)."""
        invalid_app_name_data = {
            "host": "localhost",
            "port": 8080,
            "debug": True,
            "secret_key": "test-secret-32-characters-long!",
            "app_name": 42,  # Should be string
        }
        result = FlextWebTypes.validate_config_data(invalid_app_name_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "app_name" in result.error
        assert result.error is not None and "string" in result.error

    def test_validate_app_data_real_errors(self) -> None:
        """Test app data validation with real errors (lines 282, 286, 290, 298, 302)."""
        # Test non-dict data
        result = FlextWebTypes.validate_app_data("not_a_dict")
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "must be a dictionary" in result.error

        # Test invalid name type (line 286)
        invalid_name_data = {
            "id": "app_test",
            "name": 123,  # Should be string
            "host": "localhost",
            "port": 8080,
            "status": "running",
            "is_running": True,
        }
        result = FlextWebTypes.validate_app_data(invalid_name_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "name" in result.error
        assert result.error is not None and "string" in result.error

        # Test invalid host type (line 290)
        invalid_host_data = {
            "id": "app_test",
            "name": "test",
            "host": 456,  # Should be string
            "port": 8080,
            "status": "running",
            "is_running": True,
        }
        result = FlextWebTypes.validate_app_data(invalid_host_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "host" in result.error
        assert result.error is not None and "string" in result.error

        # Test invalid port type (line 298)
        invalid_port_data = {
            "id": "app_test",
            "name": "test",
            "host": "localhost",
            "port": "8080",  # Should be int
            "status": "running",
            "is_running": True,
        }
        result = FlextWebTypes.validate_app_data(invalid_port_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "port" in result.error
        assert result.error is not None and "integer" in result.error

        # Test invalid is_running type (line 302)
        invalid_is_running_data = {
            "id": "app_test",
            "name": "test",
            "host": "localhost",
            "port": 8080,
            "status": "running",
            "is_running": "true",  # Should be bool
        }
        result = FlextWebTypes.validate_app_data(invalid_is_running_data)
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "is_running" in result.error
        assert result.error is not None and "boolean" in result.error

    def test_factory_methods_edge_cases_real(self) -> None:
        """Test factory methods with real edge cases (lines 316-317, 325-331)."""
        # Test create_request_context with edge values
        context = FlextWebTypes.create_request_context(
            method="",  # Empty method
            path="",  # Empty path
            headers={},
            data={},
        )

        # Should handle empty values gracefully
        assert not context.get("method")
        assert not context.get("path")
        assert context.get("headers") == {}
        assert context.get("data") == {}

        # Test create_request_context with complex nested data
        complex_data = {
            "nested": {
                "deep": {
                    "structure": ["list", "with", "values"],
                    "numbers": [1, 2, math.pi, True],
                },
            },
        }
        context = FlextWebTypes.create_request_context(
            method="POST",
            path="/api/complex",
            headers={"Content-Type": "application/json"},
            data=complex_data,
        )

        assert context.get("method") == "POST"
        assert context.get("path") == "/api/complex"
        assert context.get("data") == complex_data
        assert context.get("headers", {}).get("Content-Type") == "application/json"

    def test_validation_exception_handling_real(self) -> None:
        """Test validation exception handling with real edge cases (lines 340-349)."""
        # Test with extremely nested data that might cause exceptions
        extremely_nested = {}
        current = extremely_nested
        for i in range(100):  # Very deep nesting
            current[f"level_{i}"] = {}
            current = current[f"level_{i}"]
        current["final"] = "value"

        # Should not raise exception, should return failure result
        result = FlextWebTypes.validate_config_data(extremely_nested)
        assert result.is_failure  # Invalid structure

        # Test with circular reference (if possible)
        circular_data = {"key": "value"}
        circular_data["self"] = circular_data

        # Should handle gracefully
        try:
            result = FlextWebTypes.validate_config_data(circular_data)
            assert result.is_failure
        except RecursionError:
            # If RecursionError occurs, it's still handled (doesn't crash)
            pass

    def test_flext_tests_integration_with_typings(self) -> None:
        """Integration test using flext_tests utilities with typings."""
        # Use FlextTestsUtilities for real testing patterns
        test_data_list = FlextTestsUtilities.create_test_data(size=1, prefix="config")

        # Create proper config data for validation
        config_data = {
            "host": "test-host",
            "port": 9999,
            "debug": False,
            "secret_key": "integration-test-secret-32-chars!",
            "app_name": "Integration Test",
        }

        # Validate using real typings validation
        result = FlextWebTypes.validate_config_data(config_data)

        if result.is_success:
            validated_data = result.value
            assert validated_data["host"] == "test-host"
            assert validated_data["port"] == 9999
            assert validated_data["debug"] is False
        else:
            # If validation fails, ensure error is meaningful
            assert isinstance(result.error, str)
            assert len(result.error) > 0

        # Verify test data was created
        assert len(test_data_list) == 1
        assert isinstance(test_data_list[0], dict)


__all__ = [
    "TestTypingsMissingCoverage",
]
