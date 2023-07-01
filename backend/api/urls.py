from django.urls import path

from .views import ShortLinkView

VERSION = '1'


urlpatterns = [
    path('links/', ShortLinkView.as_view())
]
