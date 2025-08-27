"""Legacy type aliases facade - backward compatibility for flext-web.

This module provides backward compatibility for type aliases that have been
consolidated into typings.py. Following the FLEXT architectural patterns for
gradual migration without breaking existing imports.

All aliases here are deprecated and redirect to typings.py.
Modern code should import directly from typings module.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Import consolidated types from typings (SINGLE SOURCE OF TRUTH)
from flext_web.typings import FlextWebTypes

# Module-level deprecated alias
type TemplateGlobal = object


def deprecation_warning(old_import: str, new_import: str) -> None:
    """Issue a deprecation warning for legacy type alias imports."""
    warnings.warn(
        f"Importing '{old_import}' from type_aliases is deprecated, use 'from flext_web.typings import {new_import}' instead",
        DeprecationWarning,
        stacklevel=3,
    )


# =============================================================================
# DEPRECATED FACADE CLASS - Use FlextWebTypes from typings.py instead
# =============================================================================


class FlextWebTypeAliases:
    """DEPRECATED: Legacy facade for FlextWebTypes.

    Use FlextWebTypes from typings.py instead.
    This class provides backward compatibility only.
    """

    def __init__(self) -> None:
        deprecation_warning("FlextWebTypeAliases", "FlextWebTypes")

    # Redirect all class attributes to FlextWebTypes
    ValidatorFunc = FlextWebTypes.ValidatorFunc
    ValidatorGenerator = FlextWebTypes.ValidatorGenerator
    RequestContext = FlextWebTypes.RequestContext
    ResponseData = FlextWebTypes.ResponseData
    TemplateContext = FlextWebTypes.TemplateContext
    ConfigValue = FlextWebTypes.ConfigValue
    ConfigDict = FlextWebTypes.ConfigDict
    ErrorDetails = FlextWebTypes.ErrorDetails
    SchemaDict = FlextWebTypes.SchemaDict
    TemplateFilter = FlextWebTypes.TemplateFilter
    HTTPStatus = FlextWebTypes.HTTPStatus

    # TypedDict aliases - redirect to FlextWebTypes
    FieldKwargs = FlextWebTypes.FieldKwargs
    AppDataDict = FlextWebTypes.AppDataDict
    ResponseDataDict = FlextWebTypes.ResponseDataDict
    ApiResponseDict = FlextWebTypes.ApiResponseDict
    AppListDataDict = FlextWebTypes.AppListDataDict
    AppListResponseDict = FlextWebTypes.AppListResponseDict
    HealthResponseDict = FlextWebTypes.HealthResponseDict
    HealthDataDict = FlextWebTypes.HealthDataDict


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES AT MODULE LEVEL
# =============================================================================

# Type aliases for backward compatibility
ValidatorFunc = FlextWebTypes.ValidatorFunc
ValidatorGenerator = FlextWebTypes.ValidatorGenerator
RequestContext = FlextWebTypes.RequestContext
ResponseData = FlextWebTypes.ResponseData
TemplateContext = FlextWebTypes.TemplateContext
ConfigValue = FlextWebTypes.ConfigValue
ConfigDict = FlextWebTypes.ConfigDict
ErrorDetails = FlextWebTypes.ErrorDetails
SchemaDict = FlextWebTypes.SchemaDict
TemplateFilter = FlextWebTypes.TemplateFilter
HTTPStatus = FlextWebTypes.HTTPStatus

# TypedDict aliases for backward compatibility
FieldKwargs = FlextWebTypes.FieldKwargs
AppDataDict = FlextWebTypes.AppDataDict
ResponseDataDict = FlextWebTypes.ResponseDataDict
ApiResponseDict = FlextWebTypes.ApiResponseDict
AppListDataDict = FlextWebTypes.AppListDataDict
AppListResponseDict = FlextWebTypes.AppListResponseDict
HealthResponseDict = FlextWebTypes.HealthResponseDict
HealthDataDict = FlextWebTypes.HealthDataDict


# Export all types for backward compatibility
__all__ = [
    "ApiResponseDict",
    "AppDataDict",
    "AppListDataDict",
    "AppListResponseDict",
    "ConfigDict",
    "ConfigValue",
    "ErrorDetails",
    "FieldKwargs",
    "FlextWebTypeAliases",
    "HTTPStatus",
    "HealthDataDict",
    "HealthResponseDict",
    "RequestContext",
    "ResponseData",
    "ResponseDataDict",
    "SchemaDict",
    "TemplateContext",
    "TemplateFilter",
    "TemplateGlobal",
    "ValidatorFunc",
    "ValidatorGenerator",
]
