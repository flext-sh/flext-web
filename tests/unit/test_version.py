from __future__ import annotations

from flext_web.__version__ import (
    FlextWebVersion,
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
    _VersionMetadata,
)


def test_version_globals() -> None:
    assert isinstance(__version__, str)
    assert isinstance(__version_info__, tuple)


def test_version_initialization_without_license() -> None:
    version = FlextWebVersion(
        _VersionMetadata(
            version="1.0.0",
            version_info=(1, 0, 0),
            title="FLEXT Web",
            description="Generic HTTP Service",
            author="FLEXT Team",
            author_email="flext@example.com",
            license_type=None,
            url="https://github.com/flext/flext-web",
        )
    )

    assert version.license == ""


def test_metadata_constants() -> None:
    assert isinstance(__title__, str)
    assert isinstance(__description__, str)
    assert isinstance(__author__, str)
    assert isinstance(__author_email__, str)
    assert isinstance(__license__, str)
    assert isinstance(__url__, str)
