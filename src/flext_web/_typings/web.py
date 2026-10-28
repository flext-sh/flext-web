"""Web-domain type aliases for flext-web.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Mapping, MutableMapping, Sequence

from flext_cli import t


class FlextWebTypingsWeb:
    """Web-domain aliases composed into the public typings facade."""

    type RequestDict = MutableMapping[
        str,
        t.Scalar | Sequence[str] | t.ConfigurationMapping,
    ]
    type ResponseDict = MutableMapping[
        str,
        t.Scalar | Sequence[str] | t.ConfigurationMapping,
    ]
    type FastApiEndpointPayload = Mapping[str, str | bool]


__all__: list[str] = ["FlextWebTypingsWeb"]
