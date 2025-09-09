"""Real CLI Entry Point Tests - NO MOCKS, REAL EXECUTION.

Tests the CLI entry point functionality with real argument parsing,
real configuration, and actual service execution.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import subprocess
import sys
from typing import TYPE_CHECKING

import pytest

from flext_web import (
    FlextWebConfigs,
    __main__ as main_module,
)

if TYPE_CHECKING:
    from subprocess import CompletedProcess


class TestRealMainEntry:
    """Test real CLI entry point functionality."""

    @pytest.mark.integration
    def test_real_help_command(self) -> None:
        """Test real help command execution."""
        result: CompletedProcess[str] = subprocess.run(
            [sys.executable, "-m", "flext_web", "--help"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()
        assert "enterprise web interface" in result.stdout.lower()
        assert "--host" in result.stdout
        assert "--port" in result.stdout
        assert "--debug" in result.stdout

    @pytest.mark.integration
    def test_real_version_command(self) -> None:
        """Test real version command execution."""
        result: CompletedProcess[str] = subprocess.run(
            [sys.executable, "-c", "import flext_web; print(flext_web.__version__)"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0
        assert result.stdout.strip() == "0.9.0"

    @pytest.mark.unit
    def test_real_argument_parser_creation(self) -> None:
        """Test real argument parser creation."""
        parser = main_module.create_parser()

        # Test parser exists and has expected arguments
        assert parser is not None

        # Test help text
        help_text = parser.format_help()
        assert "enterprise web interface" in help_text.lower()
        assert "--host" in help_text
        assert "--port" in help_text
        assert "--debug" in help_text
        assert "--no-debug" in help_text

    @pytest.mark.unit
    def test_real_argument_parsing_defaults(self) -> None:
        """Test real argument parsing with default values."""
        parser = main_module.create_parser()
        args = parser.parse_args([])

        assert args.host is None  # Uses config default
        assert args.port is None  # Uses config default
        assert args.debug is False  # Default for store_true
        assert args.no_debug is False  # Default for store_true

    @pytest.mark.unit
    def test_real_argument_parsing_custom_values(self) -> None:
        """Test real argument parsing with custom values."""
        parser = main_module.create_parser()
        args = parser.parse_args(
            [
                "--host",
                "0.0.0.0",
                "--port",
                "9000",
                "--debug",
            ]
        )

        assert args.host == "0.0.0.0"  # Argument parsing preserves original value
        assert args.port == 9000
        assert args.debug is True

    @pytest.mark.unit
    def test_real_argument_parsing_no_debug(self) -> None:
        """Test real argument parsing with --no-debug flag."""
        parser = main_module.create_parser()
        args = parser.parse_args(["--no-debug"])

        assert args.debug is False

    @pytest.mark.integration
    def test_real_config_creation_from_args(self) -> None:
        """Test real configuration creation from parsed arguments."""
        # Set production environment for this test
        original_env = os.getenv("FLEXT_WEB_ENVIRONMENT")
        os.environ["FLEXT_WEB_ENVIRONMENT"] = "production"

        try:
            # Test with custom arguments
            config = FlextWebConfigs.WebConfig(
                host="test-host",
                port=9001,
                debug=False,
                secret_key="test-secret-key-32-characters-long!",
            )

            assert config.host == "test-host"
            assert config.port == 9001
            assert config.debug is False
            assert config.is_production() is True
        finally:
            # Restore original environment
            if original_env is None:
                os.environ.pop("FLEXT_WEB_ENVIRONMENT", None)
            else:
                os.environ["FLEXT_WEB_ENVIRONMENT"] = original_env

    @pytest.mark.integration
    def test_real_main_function_execution(self) -> None:
        """Test real main function execution logic."""
        # Test that main function exists and is callable
        assert hasattr(main_module, "main")
        assert callable(main_module.main)

        # Test parser creation
        parser = main_module.create_parser()
        assert parser is not None

        # Test argument parsing (don't use --help as it causes SystemExit)
        args = parser.parse_args([])
        assert hasattr(args, "host")
        assert hasattr(args, "port")

    @pytest.mark.slow
    def test_real_service_startup_validation(self) -> None:
        """Test real service startup validation."""
        result: CompletedProcess[str] = subprocess.run(
            [
                sys.executable,
                "-m",
                "flext_web",
                "--host",
                "localhost",
                "--port",
                "8082",
                "--debug",
                "--help",  # Exit immediately after showing help
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should show help and exit successfully
        assert result.returncode == 0
        assert "usage:" in result.stdout.lower()

    @pytest.mark.integration
    def test_real_cli_with_environment_variables(self) -> None:
        """Test real CLI interaction with environment variables."""
        # Save original environment
        original_host = os.environ.get("FLEXT_WEB_HOST")
        original_port = os.environ.get("FLEXT_WEB_PORT")

        try:
            # Set environment variables
            os.environ["FLEXT_WEB_HOST"] = "env-host"
            os.environ["FLEXT_WEB_PORT"] = "8090"

            # Reset to reload config
            # reset_web_settings()

            # Get configuration using settings (properly loads from environment)
            from flext_web.settings import FlextWebSettings
            settings = FlextWebSettings()
            config_result = settings.to_config()
            assert config_result.is_success
            config = config_result.value
            assert config.host == "env-host"
            assert config.port == 8090

        finally:
            # Restore original environment
            if original_host is not None:
                os.environ["FLEXT_WEB_HOST"] = original_host
            else:
                os.environ.pop("FLEXT_WEB_HOST", None)

            if original_port is not None:
                os.environ["FLEXT_WEB_PORT"] = original_port
            else:
                os.environ.pop("FLEXT_WEB_PORT", None)

            # reset_web_settings()


class TestRealCLIErrorHandling:
    """Test real CLI error handling scenarios."""

    @pytest.mark.integration
    def test_real_invalid_port_handling(self) -> None:
        """Test real handling of invalid port values."""
        result: CompletedProcess[str] = subprocess.run(
            [sys.executable, "-m", "flext_web", "--port", "99999"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should fail with invalid port
        assert result.returncode != 0
        assert "port" in result.stderr.lower() or "port" in result.stdout.lower()

    @pytest.mark.integration
    def test_real_invalid_argument_handling(self) -> None:
        """Test real handling of invalid arguments."""
        result: CompletedProcess[str] = subprocess.run(
            [sys.executable, "-m", "flext_web", "--invalid-argument"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )

        # Should fail with unrecognized argument
        assert result.returncode != 0
        assert (
            "unrecognized" in result.stderr.lower()
            or "invalid" in result.stderr.lower()
        )

    @pytest.mark.unit
    def test_real_parser_error_scenarios(self) -> None:
        """Test real parser error scenarios."""
        parser = main_module.create_parser()

        # Test invalid port (non-numeric)
        with pytest.raises(SystemExit):
            parser.parse_args(["--port", "invalid"])

        # Test valid port range (argparse accepts negative integers)
        args = parser.parse_args(["--port", "-1"])
        assert args.port == -1  # argparse allows this, validation happens later

        # Test debug flags work independently
        args1 = parser.parse_args(["--debug"])
        assert args1.debug is True
        assert args1.no_debug is False

        args2 = parser.parse_args(["--no-debug"])
        assert args2.debug is False
        assert args2.no_debug is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
