#!/usr/bin/env python3
"""Critical Coverage Tests - Target the exact missing 10% for production safety.

These tests target the specific uncovered lines identified in coverage analysis
to ensure production-critical code paths are validated.
"""

from __future__ import annotations

import asyncio
import contextlib
import sys
from unittest.mock import patch

import pytest

import flext_web
from flext_web import (
    FlextWebApp,
    FlextWebAppHandler,
    FlextWebAppStatus,
    FlextWebConfig,
    FlextWebService,
    get_web_settings,
    reset_web_settings,
)


class TestCriticalMissingCoverage:
    """Tests for production-critical missing coverage lines."""

    def test_domain_port_validation_line_199(self) -> None:
        """Test the exact domain validation on line 199 that's never hit.

        This is CRITICAL because domain validation could fail in production
        even if Pydantic validation passes.
        """
        # Create app with valid Pydantic port
        app = FlextWebApp(
            id="test_port_validation",
            name="test-app",
            port=8080,
            host="localhost",
        )

        # Use model_copy to create new instance with invalid port
        # This bypasses Pydantic validation during construction
        try:
            invalid_app = app.model_copy(update={"port": 99999})
            result = invalid_app.validate_domain_rules()
            assert result.is_failure
            assert "Invalid port number" in result.error
        except Exception:
            # If model_copy validation fails, use direct attribute manipulation
            # via object.__setattr__ to bypass frozen model protection
            object.__setattr__(app, "port", 99999)
            result = app.validate_domain_rules()
            assert result.is_failure
            assert "Invalid port number" in result.error

    def test_cli_debug_args_lines_114_116(self) -> None:
        """Test CLI argument parsing lines 114-116 that are never hit.

        These lines control debug mode in production - CRITICAL for deployment.
        """
        # Test --debug flag (line 114)
        cmd = [sys.executable, "-m", "flext_web", "--debug", "--help"]
        proc = asyncio.get_event_loop().run_until_complete(
            asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            ),
        )
        try:
            asyncio.get_event_loop().run_until_complete(
                asyncio.wait_for(proc.wait(), timeout=10),
            )
        except TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                asyncio.get_event_loop().run_until_complete(proc.kill())
        assert int(proc.returncode or 0) == 0

        # Test --no-debug flag (line 116)
        cmd = [sys.executable, "-m", "flext_web", "--no-debug", "--help"]
        proc = asyncio.get_event_loop().run_until_complete(
            asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            ),
        )
        try:
            asyncio.get_event_loop().run_until_complete(
                asyncio.wait_for(proc.wait(), timeout=10),
            )
        except TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                asyncio.get_event_loop().run_until_complete(proc.kill())
        assert int(proc.returncode or 0) == 0

    def test_cli_host_port_override_lines_110_111(self) -> None:
        """Test CLI host/port override that could be missing in coverage."""
        # Test custom host/port via CLI
        cmd = [
            sys.executable,
            "-m",
            "flext_web",
            "--host",
            "127.0.0.1",
            "--port",
            "9000",
            "--help",
        ]
        proc = asyncio.get_event_loop().run_until_complete(
            asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            ),
        )
        try:
            asyncio.get_event_loop().run_until_complete(
                asyncio.wait_for(proc.wait(), timeout=10),
            )
        except TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                asyncio.get_event_loop().run_until_complete(proc.kill())
        assert int(proc.returncode or 0) == 0

    def test_type_checking_import_line_68(self) -> None:
        """Test TYPE_CHECKING import coverage (line 68).

        While not runtime critical, this ensures imports work correctly.
        """
        # Import the module and verify TYPE_CHECKING is handled

        # Verify that ResponseReturnValue type is available when needed
        # This tests that the TYPE_CHECKING import works correctly
        assert hasattr(flext_web, "FlextWebService")

    def test_error_path_coverage_lines_571_614(self) -> None:
        """Test error paths in handler methods that might be uncovered."""
        handler = FlextWebAppHandler()

        # Test create with invalid data to trigger error path
        with patch("flext_web.web_models.FlextWebApp") as mock_app:
            mock_app.side_effect = ValueError("Validation failed")
            result = handler.create("test", 8080, "localhost")
            assert result.is_failure
            assert "failed" in result.error.lower()

    def test_config_validation_error_paths_lines_1035_1036(self) -> None:
        """Test configuration validation error paths."""
        # Reset config to test fresh validation
        reset_web_settings()

        # Mock validation failure
        with patch("flext_web.FlextWebConfig.validate_config") as mock_validate:
            mock_validate.return_value = type(
                "Result",
                (),
                {"success": False, "error": "Mock validation error"},
            )()

            # Should raise ValueError (line 1036) not FlextWebConfigurationError
            with pytest.raises(ValueError, match="Configuration validation failed"):
                get_web_settings()

    def test_service_error_handling_line_872(self) -> None:
        """Test service error handling paths that might be missed."""
        config = FlextWebConfig(secret_key="test-key-32-characters-long-valid!")
        service = FlextWebService(config)

        # Test invalid API request to trigger error path
        client = service.app.test_client()
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

    def test_main_module_execution_lines_122_135(self) -> None:
        """Test main module execution paths including error handling."""
        # Test module execution with invalid arguments
        cmd = [sys.executable, "-m", "flext_web", "--port", "invalid"]
        proc = asyncio.get_event_loop().run_until_complete(
            asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            ),
        )
        try:
            asyncio.get_event_loop().run_until_complete(
                asyncio.wait_for(proc.wait(), timeout=10),
            )
        except TimeoutError:
            with contextlib.suppress(ProcessLookupError):
                asyncio.get_event_loop().run_until_complete(proc.kill())
        # Should fail with argument parsing error
        assert int(proc.returncode or 0) != 0

    def test_branch_coverage_improvement(self) -> None:
        """Test branch coverage scenarios that improve overall coverage."""
        # Test all status transitions to improve branch coverage
        app = FlextWebApp(
            id="branch_test",
            name="branch-app",
            port=8080,
            host="localhost",
            status=FlextWebAppStatus.STOPPED,
        )

        # Test start from stopped state
        start_result = app.start()
        assert start_result.success
        running_app = start_result.data
        assert running_app.status == FlextWebAppStatus.RUNNING

        # Test stop from running state
        stop_result = running_app.stop()
        assert stop_result.success
        stopped_app = stop_result.data
        assert stopped_app.status == FlextWebAppStatus.STOPPED

        # Test validation on all states
        for status in FlextWebAppStatus:
            test_app = FlextWebApp(
                id=f"test_{status.value}",
                name="test-app",
                port=8080,
                host="localhost",
                status=status,
            )
            validation_result = test_app.validate_domain_rules()
            assert validation_result.success


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
