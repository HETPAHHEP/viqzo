import pytest

from backend.core.enums import Limits


# БАЗОВЫЕ ФИКСТУРЫ КОРОТКИХ ССЫЛОК


@pytest.fixture()
def valid_original_link():
    link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    return {"original_link": link}


@pytest.fixture()
def invalid_original_link():
    link = "mylinktest-12345-@#!"
    return {"original_link": link}


@pytest.fixture()
def very_long_link():
    link = (
        "https://duckduckgo.com/?q="
        + "%D1%81%D0%BB%D0%BE%D0%B2%D0%BE+%D0%BD%D0%B"
        "0+%D0%B1%D1%83%D0%BA%D0%B2%D1%83+%D0%B0" * 300 + "&t=h_&ia=web"
    )
    return {"original_link": link}


# ФИКСТУРЫ ПОЛЬЗОВАТЕЛЬСКИХ ССЫЛОК


@pytest.fixture()
def original_link_with_alias():
    link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    alias = "R1ckR0ll"
    return {"original_link": link, "alias": alias}


@pytest.fixture()
def original_link_with_other_alias():
    link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    alias = "marshmallowcats"
    return {"original_link": link, "alias": alias}


@pytest.fixture()
def original_link_with_invalid_alias():
    link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    alias = "-r!ckr*ll-"
    return {"original_link": link, "alias": alias}


@pytest.fixture()
def very_long_link_with_alias():
    link = (
        "https://duckduckgo.com/?q="
        + "%D1%81%D0%BB%D0%BE%D0%B2%D0%BE+%D0%BD%D0%B"
        "0+%D0%B1%D1%83%D0%BA%D0%B2%D1%83+%D0%B0" * 300 + "&t=h_&ia=web"
    )
    alias = "verylonglink"
    return {"original_link": link, "alias": alias}


@pytest.fixture()
def very_short_alias():
    link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    alias = "a" * (Limits.MIN_LEN_LINK_SHORT_CODE - 1)
    return {"original_link": link, "alias": alias}


@pytest.fixture()
def very_long_alias():
    link = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    alias = "a" * (Limits.MAX_LEN_LINK_SHORT_CODE + 1)
    return {"original_link": link, "alias": alias}


# ФИКСТУРЫ ДЛЯ ИЗМЕНЕНИЯ ССЫЛКИ


@pytest.fixture()
def is_active_status_true_bool():
    status = True
    return {"is_active": status}


@pytest.fixture()
def is_active_status_true_num():
    status = 1
    return {"is_active": status}


@pytest.fixture()
def is_active_status_true_str_lowercase():
    status = "true"
    return {"is_active": status}


@pytest.fixture()
def is_active_status_true_str_capital():
    status = "True"
    return {"is_active": status}


@pytest.fixture()
def is_active_status_false_bool():
    status = False
    return {"is_active": status}


@pytest.fixture()
def is_active_status_false_num():
    status = 0
    return {"is_active": status}


@pytest.fixture()
def is_active_status_false_str_lowercase():
    status = "false"
    return {"is_active": status}


@pytest.fixture()
def is_active_status_false_str_capital():
    status = "False"
    return {"is_active": status}
