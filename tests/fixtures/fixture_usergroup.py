import pytest

from backend.core.enums import Limits

# ФИКСТУРЫ ПОЛЬЗОВАТЕЛЬСКИХ ГРУПП ДЛЯ ССЫЛОК


@pytest.fixture()
def name_for_usergroup():
    name_group = 'Test Name'
    return {
        'name': name_group
    }


@pytest.fixture()
def very_long_name_for_usergroup():
    name_group = 'a' * Limits.MAX_LEN_GROUP_NAME + 'a'
    return {
        'name': name_group
    }


@pytest.fixture()
def very_short_name_for_usergroup():
    name_group = 'A'
    return {
        'name': name_group
    }


@pytest.fixture()
def empty_name_for_usergroup():
    name_group = ''
    return {
        'name': name_group
    }

