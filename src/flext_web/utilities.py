"""FlextWeb-specific utilities extending flext-core patterns.

Minimal implementation providing ONLY web-domain-specific utilities not available
in flext-core. Delegates all generic operations to FlextUtilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re

from flext_core import FlextUtilities


class FlextWebUtilities(FlextUtilities):
    """Web-specific utilities delegating to flext-core.

    Inherits from FlextUtilities to avoid duplication and ensure consistency.
    Provides only web-domain-specific functionality not available in FlextUtilities.
    All generic operations delegate to FlextUtilities from flext-core.
    """

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to URL-safe slug format."""
        slug = re.sub(r"[^\w\s-]", "", text.lower())
        slug = re.sub(r"[-\s]+", "-", slug)
        return slug.strip("-")

    @staticmethod
    def format_app_id(name: str) -> str:
        """Format application name to valid ID.

        This is a minimal utility that should be used directly by Application.Entity
        when creating instances. No fallbacks - fails fast if name is invalid.

        Args:
            name: Application name to format

        Returns:
            Formatted application ID

        Raises:
            ValueError: If name cannot be formatted to valid ID

        """
        # Use flext-core TextProcessor - handle FlextResult properly
        safe_string_result = FlextUtilities.TextProcessor.safe_string(name)
        # Fast fail if safe_string fails - no fallback
        if safe_string_result.is_failure:
            error_msg = f"Invalid application name: {safe_string_result.error}"
            raise ValueError(error_msg)
        clean_name = safe_string_result.unwrap().strip()
        if not clean_name:
            error_msg = "Application name cannot be empty"
            raise ValueError(error_msg)
        slugified = FlextWebUtilities._slugify(clean_name)
        if not slugified:
            error_msg = f"Cannot format application name '{name}' to valid ID"
            raise ValueError(error_msg)
        return f"app_{slugified}"


__all__ = [
    "FlextWebUtilities",
]
