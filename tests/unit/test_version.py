"""Unit tests for flext_web.__version__ module.

Tests the FlextWebVersion class methods and module-level exports
following the canonical FlextVersion test pattern from flext-core.
"""

from __future__ import annotations

from packaging.version import Version

from flext_tests import tm

from flext_web import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)
from flext_web.__version__ import FlextWebVersion


class TestsFlextWebVersion:
    """Test suite for FlextWebVersion class."""

    def test_class_version_string(self) -> None:
        """The MRO-derived class version is a semantic version string."""
        version = FlextWebVersion.__version__
        tm.that(version, is_=str, none=False, empty=False)
        tm.that(
            version,
            match="^\\d+\\.\\d+\\.\\d+",
            msg="Version must match semantic versioning",
        )

    def test_class_version_info(self) -> None:
        """The MRO-derived class version info is a three-integer release tuple."""
        version_info = FlextWebVersion.__version_info__
        tm.that(version_info, is_=tuple, none=False, empty=False, len=3)
        tm.that(all(isinstance(component, int) for component in version_info), eq=True)
        tm.that(
            version_info[0],
            is_=int,
            gt=-1,
            msg="Major version must be non-negative integer",
        )

    def test_class_package_metadata(self) -> None:
        """The version facade publishes every package metadata field."""
        info = {
            "name": FlextWebVersion.__title__,
            "version": FlextWebVersion.__version__,
            "description": FlextWebVersion.__description__,
            "author": FlextWebVersion.__author__,
            "author_email": FlextWebVersion.__author_email__,
            "license": FlextWebVersion.__license__,
            "url": FlextWebVersion.__url__,
        }
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
            info, has=required_keys, msg="Package info must contain all required keys"
        )
        for key in required_keys:
            tm.that(
                info[key],
                is_=str,
                none=False,
                msg=f"Key {key} must be non-empty string",
            )

    def test_version_format(self) -> None:
        """The exported version info matches the PEP 440 release triple."""
        tm.that(__version_info__, eq=Version(__version__).release)

    def test_module_level_exports(self) -> None:
        """Test module-level version exports are consistent with class."""
        tm.that(
            __version__, is_=str, none=False, empty=False, match="^\\d+\\.\\d+\\.\\d+"
        )
        tm.that(__version_info__, is_=tuple, none=False, empty=False, len=3)
        tm.that(
            __version__,
            eq=FlextWebVersion.__version__,
            msg="Module export must match the version facade",
        )
        tm.that(
            __version_info__,
            eq=FlextWebVersion.__version_info__,
            msg="Module export must match the version facade",
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
