from django.shortcuts import render
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets

from lyrics.models import Artist, Album, Song, LyricRevision
from lyrics.serializers import ArtistSerializer, AlbumSerializer, SongSerializer, LyricSerializer


def home(request):
    return render(request, 'home.html')


class ArtistViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class AlbumViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SongViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(editor=self.request.user)

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user)


class LyricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LyricRevision.objects.all()
    serializer_class = LyricSerializer
