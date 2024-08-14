from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views

from .views import ShortLinkViewSet, UserGroupLinkViewSet


VERSION = "v1"

router = DefaultRouter()

router.register(r"groups", UserGroupLinkViewSet, basename="group-actions")
router.register(r"links", ShortLinkViewSet, basename="link-actions")


urlpatterns = [
    path("", include("djoser.urls")),
    # AUTH JWT
    re_path(
        r"^auth/jwt/create/?",
        views.TokenObtainPairView.as_view(),
        name="jwt-create",
    ),
    re_path(
        r"^auth/jwt/refresh/?",
        views.TokenRefreshView.as_view(),
        name="jwt-refresh",
    ),
]

urlpatterns += router.urls
