from django.urls import path

from .views import CreateShortLinkView, GetShortLinkView

VERSION = 'v1'


urlpatterns = [
    path(
        'links/',
        CreateShortLinkView.as_view(),
        name='short-link-create'
    ),
    path(
        'links/<str:short_url>/',
        GetShortLinkView.as_view(),
        name='short-link-detail'
    )
]
