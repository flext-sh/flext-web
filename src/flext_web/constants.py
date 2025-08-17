"""Constants for FLEXT Web module.

This module defines centralized constants following the FlextConstants pattern
from flext-core, extending it with web-specific constants.
"""

from __future__ import annotations

import os
import secrets

from flext_core import FlextConstants


class FlextWebConstants(FlextConstants):
    """Central container for web-specific constants.

    Follows the same pattern as FlextConstants from flext-core,
    organizing constants into logical categories with type safety.
    """

    class Network:
      """Network and port constants."""

      # Port validation ranges
      MIN_PORT = 1
      MAX_PORT = 65535

      # Common HTTP ports
      DEFAULT_HTTP_PORT = 80
      DEFAULT_HTTPS_PORT = 443
      DEFAULT_DEVELOPMENT_PORT = 8080

    class Validation:
      """Validation limits and constraints."""

      # String length limits
      MAX_APP_NAME_LENGTH = 255
      MIN_APP_NAME_LENGTH = 1
      MAX_HOST_LENGTH = 253  # RFC 1035 limit for FQDN

      # Application limits
      MAX_CONCURRENT_APPS = 100
      MIN_APP_TIMEOUT = 1
      MAX_APP_TIMEOUT = 3600  # 1 hour

    class HTTP:
      """HTTP-related constants."""

      # Status codes
      OK = 200
      CREATED = 201
      BAD_REQUEST = 400
      NOT_FOUND = 404
      INTERNAL_SERVER_ERROR = 500

      # Content types
      JSON_CONTENT_TYPE = (
          FlextConstants.Observability.SERIALIZATION_FORMAT_JSON
          if hasattr(FlextConstants.Observability, "SERIALIZATION_FORMAT_JSON")
          else "application/json"
      )
      HTML_CONTENT_TYPE = "text/html"

    class Configuration:
      """Configuration defaults."""

      # Server defaults
      DEFAULT_HOST = FlextConstants.Platform.DEFAULT_HOST
      DEFAULT_PORT = 8080
      DEFAULT_DEBUG = True

      # Flask settings (generated or provided via environment)
      DEFAULT_SECRET_KEY = os.getenv(
          "FLEXT_WEB_SECRET_KEY",
          secrets.token_urlsafe(32),
      )
      SESSION_TIMEOUT = 3600  # 1 hour
