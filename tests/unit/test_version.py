"""Unit tests for flext_web.__version__ module.

Tests the FlextWebVersion class methods and module-level exports
following the canonical FlextVersion test pattern from flext-core.
"""

from __future__ import annotations

from flext_tests import tm

from flext_web import (
    FlextWebVersion,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)


class TestFlextWebVersion:
    """Test suite for FlextWebVersion class."""

    def test_resolve_version_string(self) -> None:
        """Test resolve_version_string returns valid version string."""
        version = FlextWebVersion.resolve_version_string()
        tm.that(version, is_=str, none=False, empty=False)
        tm.that(
            version,
            match="^\\d+\\.\\d+\\.\\d+",
            msg="Version must match semantic versioning",
        )

    def test_resolve_version_info(self) -> None:
        """Test resolve_version_info returns valid version tuple."""
        version_info = FlextWebVersion.resolve_version_info()
        tm.that(version_info, is_=(tuple, list), none=False, empty=False, len=(1, 10))
        tm.that(
            version_info[0],
            is_=int,
            gt=-1,
            msg="Major version must be non-negative integer",
        )

    def test_resolve_package_info(self) -> None:
        """Test resolve_package_info returns complete package metadata."""
        info = FlextWebVersion.resolve_package_info()
        tm.that(info, is_=dict, none=False, empty=False)
        required_keys = [
            "name",
            "version",
            "description",
            "author",
            "author_email",
            "license",
            "url",
        ]
        tm.that(
            info,
            has=required_keys,
            msg="Package info must contain all required keys",
        )
        for key in required_keys:
            tm.that(
                info[key],
                is_=str,
                none=False,
                msg=f"Key {key} must be non-empty string",
            )

    def test_version_format(self) -> None:
        """Test version format is valid."""
        version_parts = __version__.split(".")
        tm.that(len(version_parts), gte=2)
        version_from_info = ".".join(str(part) for part in __version_info__)
        tm.that(version_from_info, eq=__version__)

    def test_module_level_exports(self) -> None:
        """Test module-level version exports are consistent with class."""
        tm.that(
            __version__,
            is_=str,
            none=False,
            empty=False,
            match="^\\d+\\.\\d+\\.\\d+",
        )
        tm.that(
            __version_info__,
            is_=(tuple, list),
            none=False,
            empty=False,
            len=(1, 10),
        )
        tm.that(
            __version__,
            eq=FlextWebVersion.resolve_version_string(),
            msg="Module export must match class method",
        )
        tm.that(
            __version_info__,
            eq=FlextWebVersion.resolve_version_info(),
            msg="Module export must match class method",
        )

    def test_metadata_constants(self) -> None:
        """Test that metadata constants are properly defined."""
        tm.that(__title__, is_=str)
        tm.that(__description__, is_=str)
        tm.that(__author__, is_=str)
        tm.that(__author_email__, is_=str)
        tm.that(__license__, is_=str)
        tm.that(__url__, is_=str)
        tm.that(__title__, empty=False)
        tm.that(__description__, empty=False)
        tm.that(__license__, is_=str)
        if __url__:
            tm.that("://" in __url__ or __url__.startswith("http"), eq=True)
