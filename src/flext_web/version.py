"""Project metadata for flext web."""

from __future__ import annotations

from typing import Final, cast

from flext_core.metadata import (
    FlextProjectVersion,
    build_metadata_exports,
)

_metadata = build_metadata_exports(__file__)
globals().update(_metadata)
_metadata_obj = cast("FlextProjectMetadata", _metadata["__flext_metadata__"])


class FlextWebVersion(FlextProjectVersion):
    """Structured metadata for the flext web distribution."""

    @classmethod
    def current(cls) -> FlextWebVersion:
        """Return canonical metadata loaded from pyproject.toml."""
        return cls.from_metadata(_metadata_obj)


VERSION: Final[FlextWebVersion] = FlextWebVersion.current()
__version__: Final[str] = VERSION.version
__version_info__: Final[tuple[int | str, ...]] = VERSION.version_info

for _name in tuple(_metadata):
    if _name not in {"__version__", "__version_info__"}:
        globals().pop(_name, None)

__all__ = ["VERSION", "FlextWebVersion", "__version__", "__version_info__"]
