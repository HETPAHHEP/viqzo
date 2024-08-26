import pytest
from django.core.management import call_command

from links.models import Color
from links.services.colors import __test_colors_palette


# ФИКСТУРЫ ДЛЯ ЗАПОЛНЕНИЯ БД ЦВЕТАМИ ДЛЯ ГРУПП. РАБОТАЮТ ОБЕ


@pytest.fixture(scope='function')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('init_all_colors')


# @pytest.fixture(scope='function')
# def django_db_setup(django_db_setup, django_db_blocker):
#     with django_db_blocker.unblock():
#         for color in __test_colors_palette:
#             Color.objects.create(
#                 name=color.name,
#                 color_hex=color.color_hex
#             )
