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
    # Максимальная длинна названия группы
    MAX_LEN_GROUP_NAME = 30
    # Максимальное количество коротких ссылок в группе
    MAX_LINKS_GROUP_AMOUNT = 100
    # Максимальное количество групп
    MAX_GROUPS_AMOUNT = 150
    # Максимальная длинна названия компании
    MAX_LEN_CAMPAIGN_NAME = 40
    # Максимальное количество групп в компании
    MAX_GROUPS_CAMPAIGN_AMOUNT = 10
    # Максимальное количество компаний
    MAX_CAMPAIGNS_AMOUNT = 10
