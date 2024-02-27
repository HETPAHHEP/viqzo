from django_filters import rest_framework as filters

from links.models import ShortLink


class LinkFilter(filters.FilterSet):
    """Фильтр ссылок"""
    group_id = filters.NumberFilter(field_name='group', lookup_expr='exact')

    class Meta:
        model = ShortLink
        fields = ['group']
