import pytest
from django.utils.version import get_version

assert get_version() == '4.2.2', 'Пожалуйста, используйте версию Django 4.2.2'

pytest_plugins = [
    'tests.fixtures.fixture_users',
    'tests.fixtures.fixture_short_url',
    'tests.fixtures.fixture_alias_url',
]
