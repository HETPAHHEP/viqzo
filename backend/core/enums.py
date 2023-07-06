from enum import IntEnum


class Limits(IntEnum):
    # Код для короткой ссылки
    MAX_LEN_LINK_SHORT_CODE = 7
    # Длина оригинальной ссылки
    MAX_LEN_ORIGINAL_LINK = 2000
    # Минимальная длина пользовательской ссылки
    MIN_LEN_ALIAS_CODE = 5
    # Максимальная длина пользовательской ссылки
    MAX_LEN_ALIAS_CODE = 30
