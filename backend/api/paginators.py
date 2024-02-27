from rest_framework.pagination import LimitOffsetPagination


class LinkPagination(LimitOffsetPagination):
    """Пагинация для показа всех ссылок пользователя"""
    max_limit = 25
    default_limit = 25


class GroupPagination(LimitOffsetPagination):
    """Пагинация для показа всех групп пользователя"""
    max_limit = 150
    default_limit = 150
