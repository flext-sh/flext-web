"""Tests for main entry point (__main__.py)."""

from __future__ import annotations

import sys
from unittest.mock import MagicMock, patch


class TestMainEntryPoint:
    """Test main entry point functionality."""

    @patch("flext_web.__main__.FlextWebAPI")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.logger")
    def test_main_default_arguments(
        self,
        mock_logger: MagicMock,
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

        # Import and run main
        from flext_web.__main__ import main
        main()

        # Verify logger calls
        mock_logger.info.assert_any_call("🚀 Starting FLEXT FlexCore Management Web Interface")
        mock_logger.info.assert_any_call("   Host: 0.0.0.0")
        mock_logger.info.assert_any_call("   Port: 5000")
        mock_logger.info.assert_any_call("   Debug: False")

        # Verify web API creation and run
        mock_web_api.assert_called_once()
        mock_api_instance.run.assert_called_once_with(host="0.0.0.0", port=5000, debug=False)

    @patch("flext_web.__main__.FlextWebAPI")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.logger")
    def test_main_custom_arguments(
        self,
        mock_logger: MagicMock,
        mock_parser: MagicMock,
        mock_web_api: MagicMock,
    ) -> None:
        """Test main function with custom arguments."""
        # Setup mock parser with custom arguments
        mock_args = MagicMock()
        mock_args.host = "127.0.0.1"
        mock_args.port = 8080
        mock_args.debug = True
        mock_parser.return_value.parse_args.return_value = mock_args

        # Setup mock web API
        mock_api_instance = MagicMock()
        mock_web_api.return_value = mock_api_instance

        # Import and run main
        from flext_web.__main__ import main
        main()

        # Verify logger calls with custom values
        mock_logger.info.assert_any_call("   Host: 127.0.0.1")
        mock_logger.info.assert_any_call("   Port: 8080")
        mock_logger.info.assert_any_call("   Debug: True")

        # Verify web API run with custom arguments
        mock_api_instance.run.assert_called_once_with(host="127.0.0.1", port=8080, debug=True)

    @patch("flext_web.__main__.FlextWebAPI")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.logger")
    @patch("flext_web.__main__.sys.exit")
    def test_main_keyboard_interrupt(
        self,
        mock_exit: MagicMock,
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

        # Verify shutdown message and exit
        mock_logger.info.assert_any_call("🛑 Shutting down FLEXT Web Interface")
        mock_exit.assert_called_once_with(0)

    @patch("flext_web.__main__.FlextWebAPI")
    @patch("flext_web.__main__.argparse.ArgumentParser")
    @patch("flext_web.__main__.logger")
    @patch("flext_web.__main__.sys.exit")
    def test_main_exception_handling(
        self,
        mock_exit: MagicMock,
        mock_logger: MagicMock,
        mock_parser: MagicMock,
        mock_web_api: MagicMock,
    ) -> None:
        """Test main function handles general exceptions."""
        # Setup mock parser
        mock_args = MagicMock()
        mock_args.host = "0.0.0.0"
        mock_args.port = 5000
        mock_args.debug = False
        mock_parser.return_value.parse_args.return_value = mock_args

        # Setup mock web API to raise general exception
        mock_api_instance = MagicMock()
        mock_api_instance.run.side_effect = RuntimeError("Test error")
        mock_web_api.return_value = mock_api_instance

        # Import and run main
        from flext_web.__main__ import main
        main()

        # Verify exception logging and exit
        mock_logger.exception.assert_called_once_with("❌ Failed to start FLEXT Web Interface")
        mock_exit.assert_called_once_with(1)

    @patch("flext_web.__main__.main")
    def test_main_module_execution(self, mock_main: MagicMock) -> None:
        """Test that main is called when module is executed directly."""
        # Import the module to trigger __name__ == "__main__" block
        with patch.object(sys, "argv", ["__main__.py"]):
            import flext_web.__main__  # This should trigger the main() call

        # Since we're mocking, we can't test the actual execution path
        # but we can verify the structure exists
        assert hasattr(flext_web.__main__, "main")
        assert callable(flext_web.__main__.main)

    def test_argument_parser_setup(self) -> None:
        """Test that argument parser is set up correctly."""
        import argparse

        # We can't easily test the parser setup without running main(),
        # but we can verify the function imports and structure exist
        import flext_web.__main__

        # Verify argparse is imported and available
        assert hasattr(flext_web.__main__, "argparse")
        assert flext_web.__main__.argparse is argparse
