# AUTO-GENERATED FILE — canonical lazy tests facade. Regenerate with: make gen
"""Test package facade exposing the project test aliases lazily."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from tests.constants import TestsFlextWebConstants as TestsFlextWebConstants, c as c
    from tests.typings import TestsFlextWebTypes as TestsFlextWebTypes, t as t
    from tests.protocols import TestsFlextWebProtocols as TestsFlextWebProtocols, p
    from tests.models import TestsFlextWebModels as TestsFlextWebModels, m as m
    from tests.utilities import TestsFlextWebUtilities as TestsFlextWebUtilities, u
    from tests.base import TestsFlextWebServiceBase as TestsFlextWebServiceBase, s as s

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": ("TestsFlextWebConstants", "c"),
        ".typings": ("TestsFlextWebTypes", "t"),
        ".protocols": ("TestsFlextWebProtocols", "p"),
        ".models": ("TestsFlextWebModels", "m"),
        ".utilities": ("TestsFlextWebUtilities", "u"),
        ".base": ("TestsFlextWebServiceBase", "s"),
    },
)

install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
