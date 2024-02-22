from rest_framework.pagination import LimitOffsetPagination


class LinksPagination(LimitOffsetPagination):
    """Пагинация для показа всех ссылок пользователя"""
    default_limit = 25
    max_limit = 25

