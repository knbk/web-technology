from django.db.models import Q
from django.shortcuts import render
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

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

    @list_route(methods=['get'])
    def search(self, request):
        query = request.GET.get('query', '')
        if not query:
            queryset = Song.objects.none()
        else:
            parts = query.split(' ')
            q = Q()
            for part in parts:
                q = q & (Q(title__icontains=part) | Q(album__title__icontains=part)
                         | Q(album__artist__name__icontains=part))
            queryset = Song.objects.filter(q)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(editor=self.request.user)

    def perform_update(self, serializer):
        serializer.save(editor=self.request.user)


class LyricViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LyricRevision.objects.all()
    serializer_class = LyricSerializer
