# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integration tests for FLEXT Web application.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from tests.integration.test_examples import (
        ExamplesFullFunctionalityTest,
        TestExamples,
        logger,
        main,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "ExamplesFullFunctionalityTest": "tests.integration.test_examples",
    "TestExamples": "tests.integration.test_examples",
    "logger": "tests.integration.test_examples",
    "main": "tests.integration.test_examples",
    "test_examples": "tests.integration.test_examples",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
