from django.urls import include, path
from rest_framework import routers

from .views import LinkViewSet

VERSION = 1

router = routers.DefaultRouter()
router.register(r'links', LinkViewSet, basename='links')

urlpatterns = [
    path('', include(router.urls))
]
