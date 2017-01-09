from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from lyrics.views import ArtistViewSet, AlbumViewSet, SongViewSet

router = DefaultRouter()
router.register('artists', ArtistViewSet)
router.register('albums', AlbumViewSet)
router.register('songs', SongViewSet)

app_name = 'api'
urlpatterns = [
    url(r'', include(router.urls)),
]