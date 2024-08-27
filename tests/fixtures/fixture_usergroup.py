from random import choices

import pytest

from backend.core.enums import Limits


# ФИКСТУРЫ ПОЛЬЗОВАТЕЛЬСКИХ ГРУПП ДЛЯ ССЫЛОК


@pytest.fixture()
def name_for_usergroup():
    name_group = "Test Name"
    return {"name": name_group}


@pytest.fixture()
def new_name_for_usergroup():
    name_group = "New Name"
    return {"name": name_group}


@pytest.fixture()
def very_long_name_for_usergroup():
    name_group = "a" * Limits.MAX_LEN_GROUP_NAME + "a"
    return {"name": name_group}


@pytest.fixture()
def very_short_name_for_usergroup():
    name_group = "A"
    return {"name": name_group}


@pytest.fixture()
def empty_name_for_usergroup():
    name_group = ""
    return {"name": name_group}


@pytest.fixture()
def all_full_limit_groups() -> list[dict]:
    alphabet = 'qwertyuiopasdfghjklzxcvbnm'
    nums = '1234567890'
    groups = []

    for _ in range(Limits.MAX_GROUPS_AMOUNT):
        group_name = ''.join(
            choices(alphabet, k=(Limits.MAX_LEN_GROUP_NAME // 2)) +
            choices(nums, k=(Limits.MAX_LEN_GROUP_NAME // 2))
        )
        groups.append({'name': group_name})

    return groups
