from django.conf.urls import url

from lyrics.views import ArtistListView, ArtistDetailView, AlbumDetailView, SongDetailView, home, SearchView

app_name = 'lyrics'
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^artists/', ArtistListView.as_view(), name='artist-list'),
    url(r'^artists/(?P<pk>\d+)/$', ArtistDetailView.as_view(), name='artist-detail'),
    url(r'^albums/(?P<pk>\d+)/$', AlbumDetailView.as_view(), name='album-detail'),
    url(r'^songs/(?P<pk>\d+)/$', SongDetailView.as_view(), name='song-detail'),
    url(r'^search/$', SearchView.as_view(), name='song-search'),
]
