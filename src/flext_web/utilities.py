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


class FlextWebUtilities(FlextUtilities):
    """Web-specific utilities delegating to flext-core.

    Inherits from FlextUtilities and ensures consistency.
    Provides only web-domain-specific functionality not available in u.
    All generic operations delegate to flext-core utilities.
    Uses advanced builder/DSL patterns for composition.
    """

    @staticmethod
    def slugify(text: str) -> str:
        """Convert text to URL-safe slug using advanced DSL builders.

        Uses chain_builder with norm, filt, mp, and norm_join for fluent composition.
        """

        # DSL: chain_builder → norm → clean → split → filt → mp → join
        def norm_lower(t: object) -> str:
            """Normalize to lowercase."""
            s = str(t) if t else ""
            return u.norm(s).str(case="lower", default="").build() or ""

        def clean_special(n: object) -> str:
            """Remove special chars, keep word chars, spaces, hyphens."""
            s = str(n) if n else ""
            return re.sub(r"[^\w\s-]", "", s) if s else ""

        def split_words(c: object) -> list[str]:
            """Split on hyphens/spaces."""
            s = str(c) if c else ""
            return re.split(r"[-\s]+", s) if s else []

        def filt_truthy(p: object) -> list[str]:
            """Filter truthy parts."""
            lst = p if isinstance(p, list) else []
            return cast("list[str]", u.filt(lst).truthy().build()) or []

        def mp_str(fp: object) -> list[str]:
            """Map to strings."""
            lst = fp if isinstance(fp, list) else []
            return cast("list[str]", u.mp(lst).str().build()) or []

        def join_hyphen(sl: object) -> str:
            """Join with hyphens."""
            lst = sl if isinstance(sl, list) else []
            return u.norm_join(cast("list[str]", lst), sep="-") or ""

        return (
            u.chain_builder(text)
            .then(norm_lower)
            .then(clean_special)
            .then(split_words)
            .then(filt_truthy)
            .then(mp_str)
            .then(join_hyphen)
            .build()
        ) or ""

    @staticmethod
    def format_app_id(name: str) -> str:
        """Format app name to valid ID using advanced DSL builders.

        Uses chain_builder with safe, validate, slugify, and norm_join.
        Fails fast if name is invalid (no fallbacks).

        Args:
            name: Application name to format

        Returns:
            Formatted application ID (prefixed with "app_")

        Raises:
            ValueError: If name cannot be formatted to valid ID

        """

        # DSL: chain_builder → safe → validate → slugify → prefix
        def safe_clean(n: object) -> str:
            """Safely clean using Text."""
            s = str(n) if n else ""
            cleaned = u.whn(s).safe(lambda x: u.Text.safe_string(str(x))).build()
            if cleaned is None:
                msg = f"Invalid application name: {name}"
                raise ValueError(msg)
            return cast("str", cleaned)

        def validate_non_empty(n: object) -> str:
            """Validate non-empty using validate_builder."""
            s = str(n) if n else ""
            validated = u.validate_builder(s).truthy().str(default="").build()
            if not validated or not isinstance(validated, str):
                msg = f"Invalid application name: {name}"
                raise ValueError(msg)
            # Additional validation using u.validate
            result = u.validate(
                validated,
                u.V.string.non_empty,
                field_name="application_name",
            )
            if result.is_failure:
                msg = f"Application name cannot be empty: {name}"
                raise ValueError(msg)
            return result.value

        def slugify_name(n: object) -> str:
            """Slugify validated name."""
            s = str(n) if n else ""
            slug = FlextWebUtilities.slugify(s)
            if not slug:
                msg = f"Cannot format application name '{name}' to valid ID"
                raise ValueError(msg)
            return slug

        def prefix_app(slug: object) -> str:
            """Add app prefix."""
            s = str(slug) if slug else ""
            return u.norm_join(["app", s], sep="_")

        return (
            u.chain_builder(name)
            .then(safe_clean)
            .then(validate_non_empty)
            .then(slugify_name)
            .then(prefix_app)
            .build()
        ) or ""


__all__ = [
    "FlextWebUtilities",
]
