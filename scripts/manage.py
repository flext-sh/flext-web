#!/usr/bin/env python
"""Django's command-line utility for REDACTED_LDAP_BIND_PASSWORDistrative tasks.

Provides Django management commands for running the web application,
database migrations, static file collection, and REDACTED_LDAP_BIND_PASSWORDistrative tasks.

Examples:
--------
    Basic module usage:

    ```python
    python manage.py runserver
    python manage.py migrate
    ```

Note:
----
    Standard Django management entry point for web application REDACTED_LDAP_BIND_PASSWORDistration.


"""

import os
import sys

from django.core.management import execute_from_command_line


def main() -> None:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "flext_web.flext_web_legacy.settings.development",
    )
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
