from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from lyrics.views import ArtistViewSet

router = DefaultRouter()
router.register('artists', ArtistViewSet)

app_name = 'api'
urlpatterns = [
    url(r'', include(router.urls)),
]