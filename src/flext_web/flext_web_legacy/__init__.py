"""FLEXT Web main package for Django web application.

This module provides the main package initialization for the FLEXT Meltano Enterprise
web application, setting up Celery integration and ensuring proper app startup.

Features:
            - Celery app integration for async task processing
    - Django app initialization
    - Shared task setup for distributed processing

Note:
----
    Initializes Django web application with Celery integration for distributed task processing.


"""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# from flext_web.flext_web_legacy.celery import app as celery_app
# TODO: Install celery dependency

# __all__ = ("celery_app",)
