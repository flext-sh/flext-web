"""Service base for flext-web tests."""

from __future__ import annotations

from typing import override

from flext_tests import s as tests_s
from flext_web import m
from tests.settings import TestsFlextWebSettings


class TestsFlextWebServiceBase(tests_s):
    """Web test service base with source and test settings namespaces."""

    # NOTE (multi-agent): flext-tests owns fetch_settings; this project
    # declares only its more-specific bootstrap settings type.
    @classmethod
    @override
    def _runtime_bootstrap_options(cls) -> p.RuntimeBootstrapOptions:
        return m.RuntimeBootstrapOptions(settings_type=TestsFlextWebSettings)


s = TestsFlextWebServiceBase

__all__: list[str] = ["TestsFlextWebServiceBase", "s"]
