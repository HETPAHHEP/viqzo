from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateShortLinkView, LinkActionsView, UserGroupLinkViewSet

VERSION = 'v1'

router = DefaultRouter()
router.register(r'groups', UserGroupLinkViewSet, basename='group-actions')


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

urlpatterns += router.urls
