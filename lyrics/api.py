from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from lyrics.views import ArtistViewSet, AlbumViewSet, SongViewSet, LyricViewSet

router = DefaultRouter()
router.register('artists', ArtistViewSet)
router.register('albums', AlbumViewSet)
router.register('songs', SongViewSet)
router.register('lyrics', LyricViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
