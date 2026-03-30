# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integration tests for FLEXT Web application.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.integration import test_examples as test_examples
    from tests.integration.test_examples import (
        ExamplesFullFunctionalityTest as ExamplesFullFunctionalityTest,
        TestExamples as TestExamples,
        logger as logger,
        main as main,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "ExamplesFullFunctionalityTest": [
        "tests.integration.test_examples",
        "ExamplesFullFunctionalityTest",
    ],
    "TestExamples": ["tests.integration.test_examples", "TestExamples"],
    "logger": ["tests.integration.test_examples", "logger"],
    "main": ["tests.integration.test_examples", "main"],
    "test_examples": ["tests.integration.test_examples", ""],
}

_EXPORTS: Sequence[str] = [
    "ExamplesFullFunctionalityTest",
    "TestExamples",
    "logger",
    "main",
    "test_examples",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
