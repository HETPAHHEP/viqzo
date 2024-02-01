import pytest

from backend.core.enums import Limits

# ФИКСТУРЫ ПОЛЬЗОВАТЕЛЬСКИХ ССЫЛОК

@pytest.fixture()
def original_link_with_alias():
    link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    alias = 'R1ckR0ll'
    return {
        'original_link': link,
        'alias': alias
    }


@pytest.fixture()
def original_link_with_invalid_alias():
    link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    alias = '-r!ckr*ll-'
    return {
        'original_link': link,
        'alias': alias
    }


@pytest.fixture()
def very_long_link_with_alias():
    link = 'https://duckduckgo.com/?q=' + \
           '%D1%81%D0%BB%D0%BE%D0%B2%D0%BE+%D0%BD%D0%B' \
           '0+%D0%B1%D1%83%D0%BA%D0%B2%D1%83+%D0%B0' * 300 + \
           '&t=h_&ia=web'
    alias = 'verylonglink'
    return {
        'original_link': link,
        'alias': alias
    }


@pytest.fixture()
def very_short_alias():
    link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    alias = 'a' * (Limits.MIN_LEN_ALIAS_CODE - 1)
    return {
        'original_link': link,
        'alias': alias
    }


@pytest.fixture()
def very_long_alias():
    link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    alias = 'a' * (Limits.MAX_LEN_ALIAS_CODE + 1)
    return {
        'original_link': link,
        'alias': alias
    }
