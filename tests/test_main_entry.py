"""Tests for main entry point (__main__.py)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch


class TestMainEntryPoint:
    """Test main entry point functionality."""

    @patch("flext_web.__main__.WebAPI")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.get_logger")
    def test_main_default_arguments(
        self,
        mock_get_logger: MagicMock,
        mock_parser: MagicMock,
        mock_web_api: MagicMock,
    ) -> None:
        """Test main function with default arguments."""
        # Setup mock parser
        mock_args = MagicMock()
        mock_args.host = "0.0.0.0"
        mock_args.port = 5000
        mock_args.debug = False
        mock_parser.return_value.parse_args.return_value = mock_args

        # Setup mock web API
        mock_api_instance = MagicMock()
        mock_web_api.return_value = mock_api_instance

        # Setup mock logger
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        # Import and run main
        from flext_web.__main__ import main

        main()

        # Verify web API creation and run
        mock_web_api.assert_called_once()
        mock_api_instance.run.assert_called_once_with(
            host="0.0.0.0",
            port=5000,
            debug=False,
        )

    @patch("flext_web.__main__.WebAPI")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.logger")
    def test_main_keyboard_interrupt(
        self,
        mock_logger: MagicMock,
        mock_parser: MagicMock,
        mock_web_api: MagicMock,
    ) -> None:
        """Test main function handles KeyboardInterrupt gracefully."""
        # Setup mock parser
        mock_args = MagicMock()
        mock_args.host = "0.0.0.0"
        mock_args.port = 5000
        mock_args.debug = False
        mock_parser.return_value.parse_args.return_value = mock_args

        # Setup mock web API to raise KeyboardInterrupt
        mock_api_instance = MagicMock()
        mock_api_instance.run.side_effect = KeyboardInterrupt()
        mock_web_api.return_value = mock_api_instance

        # Import and run main
        from flext_web.__main__ import main

        main()

        # Verify shutdown message
        mock_logger.info.assert_any_call("🛑 Shutting down FLEXT Web Interface")
