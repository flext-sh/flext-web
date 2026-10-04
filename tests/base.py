"""Service base for flext-web tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_tests import FlextTestsServiceBase

from flext_web import m
from tests import TestsFlextWebSettings


class TestsFlextWebServiceBase(FlextTestsServiceBase):
    """Web test service base with source and test settings namespaces."""

    # NOTE (multi-agent): flext-tests owns fetch_settings; this project
    # declares only its more-specific bootstrap settings type.
    @classmethod
    @override
    def runtime_bootstrap_options(cls) -> m.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextWebSettings)


s = TestsFlextWebServiceBase

__all__: list[str] = ["TestsFlextWebServiceBase", "s"]
