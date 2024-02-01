from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateGroupView, CreateGroupViewSet, CreateShortLinkView,
                    LinkActionsView)

VERSION = 'v1'

router = DefaultRouter()
# router.register(r'groups', CreateGroupViewSet, basename='groups')


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path('links/', CreateShortLinkView.as_view(), name='link-create'),
    path(
        'links/<str:short_url>/',
        LinkActionsView.as_view(),
        name='link-actions'
    ),
    path('groups/', CreateGroupView.as_view(), name='group-create'),
]

urlpatterns += router.urls
