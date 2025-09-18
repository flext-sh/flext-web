"""Test version module functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import flext_web.__version__ as version_module
from flext_web.__version__ import __version__


class TestVersionModule:
    """Test version module functionality."""

    def test_version_import(self) -> None:
        """Test version module can be imported and contains version info."""
        assert isinstance(__version__, str)
        assert len(__version__) > 0
        assert "." in __version__  # Should be in format like "0.9.0"

    def test_version_format(self) -> None:
        """Test version follows semantic versioning format."""
        # Basic semantic version validation
        parts = __version__.split(".")
        assert len(parts) >= 2  # At least major.minor

        # First two parts should be numeric
        assert parts[0].isdigit()
        assert parts[1].isdigit()

    def test_version_accessibility(self) -> None:
        """Test version is accessible through main module."""
        # Test direct import

        assert hasattr(version_module, "__version__")
        assert isinstance(version_module.__version__, str)

        # Test version is not empty or placeholder
        assert version_module.__version__
        assert version_module.__version__ != "0.0.0"
