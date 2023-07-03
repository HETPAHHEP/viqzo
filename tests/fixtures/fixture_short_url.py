import pytest


@pytest.fixture()
def valid_original_link():
    link = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    return {
        'original_link': link
    }


@pytest.fixture()
def invalid_original_link():
    link = 'mylinktest-12345-@#!'
    return {
        'original_link': link
    }


@pytest.fixture()
def very_long_link():
    link = 'https://duckduckgo.com/?q=' + \
           '%D1%81%D0%BB%D0%BE%D0%B2%D0%BE+%D0%BD%D0%B' \
           '0+%D0%B1%D1%83%D0%BA%D0%B2%D1%83+%D0%B0' * 300 + \
           '&t=h_&ia=web'
    return {
        'original_link': link
    }