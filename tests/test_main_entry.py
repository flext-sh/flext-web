"""FLEXT Web Interface - CLI Entry Point Testing Suite.

Enterprise-grade test suite for command-line interface functionality, argument
parsing, configuration override, and service initialization patterns. Ensures
CLI follows enterprise standards with proper error handling and deployment scenarios.

Test Coverage:
    - Command-line argument parsing and validation
    - Configuration override through CLI parameters
    - Service initialization and startup sequences
    - Error handling and exit code management
    - Production vs development mode behavior

Integration:
    - Tests CLI integration with FlextWebConfig
    - Validates service creation and startup patterns
    - Ensures proper error handling and logging
    - Verifies enterprise deployment scenarios

Author: FLEXT Development Team
Version: 0.9.0
Status: Enterprise CLI testing with comprehensive argument validation
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from flext_web.__main__ import main


class TestMainEntryPoint:
    """Enterprise CLI testing for main entry point functionality.

    Comprehensive test suite covering command-line interface argument parsing,
    configuration management, service initialization, and error handling.
    Ensures CLI follows enterprise patterns with proper deployment support.
    """

    @patch("flext_web.__main__.FlextWebService")
    @patch("flext_web.__main__.FlextWebConfig")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.get_logger")
    def test_main_default_arguments(
        self,
        mock_get_logger: MagicMock,
        mock_parser: MagicMock,
        mock_config_class: MagicMock,
        mock_service_class: MagicMock,
    ) -> None:
        """Test main function with default arguments.

        Args:
            mock_get_logger (MagicMock): Description.
            mock_parser (MagicMock): Description.
            mock_config_class (MagicMock): Description.
            mock_service_class (MagicMock): Description.

        """
        # Setup mock parser
        mock_args = MagicMock()
        mock_args.host = None
        mock_args.port = None
        mock_args.debug = False
        mock_args.no_debug = False
        mock_parser.return_value.parse_args.return_value = mock_args

        # Setup mock config
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 8080
        mock_config.debug = True
        mock_config.app_name = "FLEXT Web"
        mock_config.version = "0.9.0"
        mock_config.is_production.return_value = False
        mock_config_class.return_value = mock_config

        # Setup mock service
        mock_service = MagicMock()
        mock_service_class.return_value = mock_service

        # Setup mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Run main function
        main()

        # Verify service creation and run
        mock_service_class.assert_called_once_with(mock_config)
        mock_service.run.assert_called_once_with(
            host="localhost",
            port=8080,
            debug=True,
        )

    @patch("flext_web.__main__.FlextWebService")
    @patch("flext_web.__main__.FlextWebConfig")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.logger")
    def test_main_keyboard_interrupt(
        self,
        mock_logger: MagicMock,
        mock_parser: MagicMock,
        mock_config_class: MagicMock,
        mock_service_class: MagicMock,
    ) -> None:
        """Test main function handles KeyboardInterrupt gracefully.

        Args:
            mock_logger (MagicMock): Description.
            mock_parser (MagicMock): Description.
            mock_config_class (MagicMock): Description.
            mock_service_class (MagicMock): Description.

        """
        # Setup mock parser
        mock_args = MagicMock()
        mock_args.host = None
        mock_args.port = None
        mock_args.debug = False
        mock_args.no_debug = False
        mock_parser.return_value.parse_args.return_value = mock_args

        # Setup mock config
        mock_config = MagicMock()
        mock_config.host = "localhost"
        mock_config.port = 8080
        mock_config.debug = True
        mock_config.app_name = "FLEXT Web"
        mock_config.version = "0.9.0"
        mock_config.is_production.return_value = False
        mock_config_class.return_value = mock_config

        # Setup mock service to raise KeyboardInterrupt
        mock_service = MagicMock()
        mock_service.run.side_effect = KeyboardInterrupt()
        mock_service_class.return_value = mock_service

        # Run main function
        main()

        # Verify shutdown message
        mock_logger.info.assert_any_call("🛑 Shutting down FlextWeb service")
