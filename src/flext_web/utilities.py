"""FlextWeb-specific utilities extending flext-core patterns.

Minimal implementation providing ONLY web-domain-specific utilities not available
in flext-core. Delegates all generic operations to u.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re

from flext_core import FlextUtilities


class FlextWebUtilities(FlextUtilities):
    """Web-specific utilities delegating to flext-core.

    Inherits from FlextUtilities and ensures consistency.
    Provides only web-domain-specific functionality not available in u.
    All generic operations delegate to flext-core utilities.
    Uses advanced builder/DSL patterns for composition.
    """

    class Web:
        """Web domain namespace."""

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-safe slug using standard string operations.

        Implements slugification without relying on non-existent DSL builders.
        """
        if not text:
            return ""

        # Normalize to lowercase
        normalized = text.lower()

        # Remove special chars, keep word chars, spaces, hyphens
        cleaned = re.sub(r"[^\w\s-]", "", normalized)

        # Split on hyphens/spaces
        words = re.split(r"[-\s]+", cleaned)

        # Filter truthy parts
        truthy_words = [word for word in words if word]

        # Join with hyphens
        return "-".join(truthy_words)

    @staticmethod
    def format_app_id(name: str) -> str:
        """Format app name to valid ID using flext-core utilities.

        Uses proper validation and string operations.
        Fails fast if name is invalid (no fallbacks).

        Args:
            name: Application name to format

        Returns:
            Formatted application ID (prefixed with "app_")

        Raises:
            ValueError: If name cannot be formatted to valid ID

        """
        if not name:
            msg = f"Invalid application name: {name}"
            raise ValueError(msg)

        # Clean the name using flext-core Text utilities
        cleaned = FlextUtilities.Text.safe_string(name)
        if not cleaned:
            msg = f"Application name cannot be empty: {name}"
            raise ValueError(msg)

        # Slugify the cleaned name
        slug = FlextWebUtilities.slugify(cleaned)
        if not slug:
            msg = f"Cannot format application name '{name}' to valid ID"
            raise ValueError(msg)

        # Add app prefix
        return f"app_{slug}"


u = FlextWebUtilities
__all__ = ["FlextWebUtilities", "u"]
