from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ShortLinkViewSet, UserGroupLinkViewSet

VERSION = 'v1'

router = DefaultRouter()

router.register(r'groups', UserGroupLinkViewSet, basename='group-actions')
router.register(r'links', ShortLinkViewSet, basename='link-actions')


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
