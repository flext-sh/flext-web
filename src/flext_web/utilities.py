"""FlextWeb-specific utilities extending flext-core patterns.

Minimal implementation providing ONLY web-domain-specific utilities not available
in flext-core. Delegates all generic operations to u.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from typing import cast

from flext_core import FlextUtilities

# Import uplified usage
u = FlextUtilities


class FlextWebUtilities(u):
    """Web-specific utilities delegating to flext-core.

    Inherits from FlextUtilities and ensures consistency.
    Provides only web-domain-specific functionality not available in u.
    All generic operations delegate to flext-core utilities.
    Uses advanced builder/DSL patterns for composition.
    """

    @staticmethod
    def _slugify(text: str) -> str:  # noqa: C901
        """Convert text to URL-safe slug format using advanced DSL builders.

        Uses advanced DSL: chain_builder() → norm().str() → filt().truthy() → mp().str() → norm_join().
        """
        # DSL pattern: chain_builder for fluent composition
        def normalize_text(t: object) -> str:
            """Normalize text to lowercase."""
            if not isinstance(t, str):
                return ""
            normalized = u.norm(t).str(case="lower", default="").build()
            return normalized if isinstance(normalized, str) else ""

        def clean_text(n: object) -> str:
            """Clean text removing special chars."""
            if not isinstance(n, str):
                return ""
            return re.sub(r"[^\w\s-]", "", n) if n else ""

        def split_text(c: object) -> list[str]:
            """Split text into parts."""
            if not isinstance(c, str):
                return []
            return re.split(r"[-\s]+", c) if c else []

        def filter_parts(p: object) -> list[str]:
            """Filter truthy parts."""
            if not isinstance(p, list):
                return []
            filtered = u.filt(cast("list[object]", p)).truthy().build()
            return cast("list[str]", filtered) if isinstance(filtered, list) else []

        def convert_to_str(fp: object) -> list[str]:
            """Convert parts to strings."""
            if not isinstance(fp, list):
                return []
            mapped = u.mp(cast("list[str]", fp)).str().build()
            return cast("list[str]", mapped) if isinstance(mapped, list) else []

        def join_slug(sl: object) -> str:
            """Join slug parts."""
            if not isinstance(sl, list):
                return ""
            return u.norm_join(cast("list[str]", sl), sep="-") if sl else ""

        result = (
            u.chain_builder(text)
            .then(normalize_text)
            .then(clean_text)
            .then(split_text)
            .then(filter_parts)
            .then(convert_to_str)
            .then(join_slug)
            .build()
        )
        return result if isinstance(result, str) else ""

    @staticmethod
    def format_app_id(name: str) -> str:  # noqa: C901
        """Format application name to valid ID using advanced DSL builders.

        Uses advanced DSL: whn().safe() → validate() → _slugify() → norm_join().
        Fails fast if name is invalid (no fallbacks).

        Args:
            name: Application name to format

        Returns:
            Formatted application ID (prefixed with "app_")

        Raises:
            ValueError: If name cannot be formatted to valid ID

        """
        # DSL pattern: chain_builder for fluent composition with error handling
        def safe_clean(n: object) -> str:
            """Safely clean name using TextProcessor."""
            if not isinstance(n, str):
                msg = f"Invalid application name: {name}"
                raise TypeError(msg)
            # Use whn().safe() for exception handling
            cleaned = u.whn(n).safe(lambda x: u.TextProcessor.safe_string(str(x))).build()
            if cleaned is None:
                msg = f"Invalid application name: {name}"
                raise ValueError(msg)
            return cast("str", cleaned)

        def validate_name(n: object) -> str:
            """Validate name is non-empty using validate_builder."""
            if not isinstance(n, str):
                msg = f"Invalid application name: {name}"
                raise TypeError(msg)
            # DSL pattern: validate_builder for fluent validation
            validated = u.validate_builder(n).truthy().str(default="").build()
            if not validated or not isinstance(validated, str):
                msg = f"Invalid application name: {name}"
                raise ValueError(msg)
            # Additional validation using u.validate for field-level checks
            result = u.validate(validated, u.V.string.non_empty, field_name="application_name")
            if result.is_failure:
                msg = f"Application name cannot be empty: {name}"
                raise ValueError(msg)
            return result.value

        def slugify_name(n: object) -> str:
            """Slugify validated name."""
            if not isinstance(n, str):
                msg = f"Invalid application name: {name}"
                raise TypeError(msg)
            slug = FlextWebUtilities._slugify(n)
            if not slug:
                msg = f"Cannot format application name '{name}' to valid ID"
                raise ValueError(msg)
            return slug

        def prefix_app(slug: object) -> str:
            """Add app prefix."""
            if not isinstance(slug, str):
                msg = f"Invalid application name: {name}"
                raise TypeError(msg)
            return u.norm_join(["app", slug], sep="_")

        # Use chain_builder for fluent composition
        result = (
            u.chain_builder(name)
            .then(safe_clean)
            .then(validate_name)
            .then(slugify_name)
            .then(prefix_app)
            .build()
        )
        return result if isinstance(result, str) else ""


__all__ = [
    "FlextWebUtilities",
]
