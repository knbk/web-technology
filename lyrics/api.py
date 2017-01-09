from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from lyrics.views import ArtistViewSet, AlbumViewSet, SongViewSet, LyricViewSet, api_root

router = DefaultRouter()
router.register('artists', ArtistViewSet)
router.register('albums', AlbumViewSet)
router.register('songs', SongViewSet)
router.register('revisions', LyricViewSet)

urlpatterns = [
    url(r'^$', api_root, name='api-root'),
    url(r'', include(router.urls)),
]
