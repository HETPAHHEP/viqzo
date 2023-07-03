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

