import os

# Minimal settings for testing
SECRET_KEY = 'test-secret-key'
DEBUG = True

INSTALLED_APPS = [
    'moneyfx',
]

# Disable migrations during tests
MIGRATION_MODULES = {
    'djmoney': None,
    'moneyfx': None,
}

# Your existing currency settings
from ..settings import *  # noqa