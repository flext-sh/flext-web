"""Tests specifically designed to cover missing lines identified by coverage analysis.

This test file targets the exact lines that are missing coverage to achieve 99%+ coverage.
Based on coverage report, these are the missing lines:
- __main__.py: 144-145 (exception handling)
- config.py: 113-114, 122-123, 132-133, 142-143 (validation errors)
- models.py: 153-154, 165-166, 203, 223-226, 236, 446, 550 (edge cases)
"""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
from pydantic import ValidationError

from flext_web import FlextWebApp  # Import from main module to avoid local imports
from flext_web.__main__ import main
from flext_web.config import FlextWebConfig
from flext_web.models import FlextWebAppHandler, FlextWebAppStatus


class TestMainExceptionHandling:
    """Test CLI exception handling in __main__.py lines 144-145."""

    @patch("flext_web.services.FlextWebService")
    @patch("sys.argv", ["flext_web"])
    def test_service_creation_runtime_error(self, mock_service_class: Mock) -> None:
        """Test RuntimeError handling in main() - line 144."""
        mock_service_class.side_effect = RuntimeError("Service creation failed")

        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)

    @patch("flext_web.services.FlextWebService")
    @patch("sys.argv", ["flext_web"])
    def test_service_creation_value_error(self, mock_service_class: Mock) -> None:
        """Test ValueError handling in main() - line 144."""
        mock_service_class.side_effect = ValueError("Invalid configuration")

        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)

    @patch("flext_web.services.FlextWebService")
    @patch("sys.argv", ["flext_web"])
    def test_service_creation_type_error(self, mock_service_class: Mock) -> None:
        """Test TypeError handling in main() - line 144."""
        mock_service_class.side_effect = TypeError("Type mismatch")

        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)

    @patch("flext_web.services.FlextWebService")
    @patch("sys.argv", ["flext_web"])
    def test_service_run_runtime_error(self, mock_service_class: Mock) -> None:
        """Test RuntimeError during service.run() - line 144."""
        mock_service = Mock()
        mock_service.run.side_effect = RuntimeError("Service run failed")
        mock_service_class.return_value = mock_service

        with patch("sys.exit") as mock_exit:
            main()
            mock_exit.assert_called_once_with(1)


class TestConfigValidationErrors:
    """Test config.py validation error cases - lines 113-114, 122-123, 132-133, 142-143."""

    def test_invalid_version_format_direct(self) -> None:
        """Test version validation error - lines 113-114."""
        # Call the validator directly to trigger the specific error message
        with pytest.raises(ValueError, match="Invalid version format"):
            FlextWebConfig.validate_version_format("invalid-version")

    def test_empty_host_validation_direct(self) -> None:
        """Test host validation error - lines 122-123."""
        # Call the validator directly to trigger the specific error message
        with pytest.raises(ValueError, match="Host is required"):
            FlextWebConfig.validate_host("")

    def test_port_validation_direct_low(self) -> None:
        """Test port validation error (too low) - lines 132-133."""
        # Call the validator directly to bypass Pydantic constraints
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            FlextWebConfig.validate_port_range(0)

    def test_port_validation_direct_high(self) -> None:
        """Test port validation error (too high) - lines 132-133."""
        # Call the validator directly to bypass Pydantic constraints
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            FlextWebConfig.validate_port_range(65536)

    def test_secret_key_validation_direct(self) -> None:
        """Test secret key validation error - lines 142-143."""
        # Call the validator directly to trigger the specific error message
        with pytest.raises(ValueError, match="Secret key must be at least 32 characters"):
            FlextWebConfig.validate_secret_key("short")

    def test_invalid_version_format(self) -> None:
        """Test version validation error via config creation."""
        with pytest.raises(ValueError, match="Invalid version format"):
            FlextWebConfig(version="invalid-version")

    def test_empty_host_validation(self) -> None:
        """Test host validation error via config creation."""
        with pytest.raises(ValueError, match="Host is required"):
            FlextWebConfig(host="")

    def test_secret_key_too_short(self) -> None:
        """Test secret key validation error via config creation."""
        with pytest.raises(ValidationError):  # Pydantic min_length constraint
            FlextWebConfig(secret_key="short")


class TestModelsEdgeCases:
    """Test models.py edge cases - lines 153-154, 165-166, 203, 223-226, 236, 446, 550."""

    def test_flext_web_app_port_validation_direct(self) -> None:
        """Test FlextWebApp port validation error - lines 153-154."""
        # Call the validator directly to trigger the specific error message
        with pytest.raises(ValueError, match="Port must be between 1 and 65535"):
            FlextWebApp.validate_port(0)

    def test_flext_web_app_port_validation_error(self) -> None:
        """Test FlextWebApp port validation error via Pydantic."""
        with pytest.raises(ValidationError):
            FlextWebApp(
                id="app_test",
                name="test",
                host="localhost",
                port=0,  # Invalid port
                status=FlextWebAppStatus.STOPPED
            )

    def test_status_coercion_exception_handling(self) -> None:
        """Test status coercion exception - lines 165-166."""
        # Test the _coerce_status method directly with various invalid inputs
        result = FlextWebApp._coerce_status(None)
        assert result == FlextWebAppStatus.ERROR

        # Test with other invalid inputs that would cause exceptions
        result = FlextWebApp._coerce_status(object())
        assert result == FlextWebAppStatus.ERROR

        result = FlextWebApp._coerce_status(123)
        assert result == FlextWebAppStatus.ERROR

    def test_business_rules_validation_empty_host(self) -> None:
        """Test business rules validation with empty host - line 203."""
        # Create app with valid host first
        app = FlextWebApp(
            id="app_test",
            name="test",
            host="localhost",
            port=8080,
            status=FlextWebAppStatus.STOPPED
        )

        # Manually set host to empty to test business rules (bypassing Pydantic validation)
        app.__dict__["host"] = ""  # Direct assignment to bypass validation

        result = app.validate_business_rules()
        assert not result.success
        assert "Host cannot be empty" in result.error

    def test_status_enum_exception_handling(self) -> None:
        """Test _status_enum exception handling - lines 223-226."""
        app = FlextWebApp(
            id="app_test",
            name="test",
            host="localhost",
            port=8080,
            status=FlextWebAppStatus.STOPPED
        )

        # Directly set status to invalid value to trigger exception path
        app.status = "invalid_status"  # type: ignore[assignment]

        # The _status_enum should handle exception and return ERROR
        result = app._status_enum()
        assert result == FlextWebAppStatus.ERROR

    def test_status_name_property(self) -> None:
        """Test status_name property - line 236."""
        app = FlextWebApp(
            id="app_test",
            name="test",
            host="localhost",
            port=8080,
            status=FlextWebAppStatus.RUNNING
        )

        # This should exercise the status_name property
        assert app.status_name == "RUNNING"

    def test_handler_create_domain_validation_failure(self) -> None:
        """Test handler creation with domain validation failure - line 446."""
        handler = FlextWebAppHandler()

        # Mock validate_business_rules to fail during creation
        with patch.object(FlextWebApp, "validate_business_rules") as mock_validate:
            mock_validate.return_value = Mock(success=False, error="Domain validation failed")

            result = handler.create("test-app", host="localhost")
            assert not result.success
            assert "Domain validation failed" in result.error

    def test_handler_stop_validation_failure(self) -> None:
        """Test handler stop with validation failure - line 550."""
        handler = FlextWebAppHandler()
        app = FlextWebApp(
            id="app_test",
            name="test",
            host="localhost",
            port=8080,
            status=FlextWebAppStatus.RUNNING
        )

        # Mock validate_domain_rules at the class level to fail
        with patch.object(FlextWebApp, "validate_domain_rules") as mock_validate:
            mock_validate.return_value = Mock(success=False, error="Validation failed")

            result = handler.stop(app)
            assert not result.success
            assert "Validation failed" in result.error


class TestAdditionalEdgeCases:
    """Additional edge cases for maximum coverage."""

    def test_flext_web_app_with_whitespace_host(self) -> None:
        """Test business rules validation with whitespace-only host."""
        # Create app with valid host first
        app = FlextWebApp(
            id="app_test",
            name="test",
            host="localhost",
            port=8080,
            status=FlextWebAppStatus.STOPPED
        )

        # Manually set host to whitespace to test business rules
        app.__dict__["host"] = "   "

        result = app.validate_business_rules()
        assert not result.success
        assert "Host cannot be empty" in result.error

    def test_status_coercion_with_various_invalid_inputs(self) -> None:
        """Test status coercion with various invalid types."""
        invalid_inputs = [None, 123, [], {}, object()]

        for invalid_input in invalid_inputs:
            result = FlextWebApp._coerce_status(invalid_input)
            assert result == FlextWebAppStatus.ERROR

    def test_config_validation_edge_cases(self) -> None:
        """Test additional config validation edge cases."""
        # Test host with only whitespace
        with pytest.raises(ValueError, match="Host is required"):
            FlextWebConfig(host="   ")

        # Test version with extra parts
        with pytest.raises(ValueError, match="Invalid version format"):
            FlextWebConfig(version="1.0.0.0")

        # Test version with non-numeric parts
        with pytest.raises(ValueError, match="Invalid version format"):
            FlextWebConfig(version="v1.0.0")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

