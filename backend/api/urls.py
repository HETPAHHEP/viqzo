from django.urls import include, path

from .views import CreateShortLinkView, LinkActionsView

VERSION = 'v1'


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('links/', CreateShortLinkView.as_view(), name='link-create'),
    path(
        'links/<str:short_url>/',
        LinkActionsView.as_view(),
        name='link-actions'
    ),
]
