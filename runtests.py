#!/usr/bin/env python

import os, sys
from django.conf import settings
import django

DEFAULT_SETTINGS = dict(
    DATABASES={
        "default": {
            "ENGINE": "django.db.backends.sqlite3"
            }
        },
    SILENCED_SYSTEM_CHECKS=["1_7.W001"],
    )

def runtests():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    # Compatibility with Django 1.7's stricter initialization
    if hasattr(django, 'setup'):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    try:
        from django.test.runner import DiscoverRunner
        runner_class = DiscoverRunner
        test_args = ['test_choices']
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        runner_class = DjangoTestSuiteRunner
        test_args = ['test_choices']

    failures = runner_class(
        verbosity=1, interactive=True, failfast=False).run_tests(test_args)
    sys.exit(failures)

if __name__ == '__main__':
    runtests()

