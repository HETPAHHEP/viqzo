import pytest
from django.core.management import call_command

from backend.core.enums import Limits


# ФИКСТУРА ДЛЯ ЗАПОЛНЕНИЯ БД ЦВЕТАМИ ДЛЯ ГРУПП
@pytest.fixture(scope='function')
def init_colors(django_db_blocker):
    with django_db_blocker.unblock():
        call_command('init_all_colors')


# ФИКСТУРЫ ДЛЯ ТЕСТОВ БИЗНЕС ЛОГИКИ ЦВЕТОВ
@pytest.fixture()
def correct_color_data() -> dict:
    name_color = 'Blue'
    color_hex = '#0000ff'

    return {
        'name': name_color,
        'color_hex': color_hex
    }


@pytest.fixture()
def empty_color_name() -> dict:
    name_color = ''
    color_hex = '#0000ff'

    return {
        'name': name_color,
        'color_hex': color_hex
    }


@pytest.fixture()
def empty_color_hex() -> dict:
    name_color = 'Blue'
    color_hex = ''

    return {
        'name': name_color,
        'color_hex': color_hex
    }


@pytest.fixture()
def empty_color_fields() -> dict:
    name_color = ''
    color_hex = ''

    return {
        'name': name_color,
        'color_hex': color_hex
    }


@pytest.fixture()
def very_long_color_name() -> dict:
    name_color = 'B' * Limits.MAX_LEN_COLOR_NAME
    color_hex = '#0000ff'

    return {
        'name': name_color,
        'color_hex': color_hex
    }


@pytest.fixture()
def very_long_color_name_over_limit() -> dict:
    name_color = 'B' * (Limits.MAX_LEN_COLOR_NAME + 1)
    color_hex = '#0000ff'

    return {
        'name': name_color,
        'color_hex': color_hex
    }


@pytest.fixture()
def very_short_color_name() -> dict:
    name_color = 'B'
    color_hex = '#0000ff'

    return {
        'name': name_color,
        'color_hex': color_hex
    }


@pytest.fixture()
def color_without_name() -> dict:
    color_hex = '#0000ff'

    return {
        'color_hex': color_hex
    }


@pytest.fixture()
def color_without_hex() -> dict:
    name_color = 'Blue'

    return {
        'name': name_color
    }


@pytest.fixture()
def color_hex_short() -> dict:
    name_color = 'Blue'
    color_hex = '#00F'

    return {
        'name': name_color,
        'color_hex': color_hex
    }
