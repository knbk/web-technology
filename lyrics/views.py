from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import list_route, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from lyrics.forms import ArtistForm, AlbumForm, SongForm
from lyrics.models import Artist, Album, Song, LyricRevision
from lyrics.serializers import ArtistSerializer, AlbumSerializer, SongSerializer, LyricSerializer


def home(request):
    return render(request, 'home.html')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'artists': reverse('artist-list', request=request, format=format),
        'albums': reverse('album-list', request=request, format=format),
        'songs': reverse('song-list', request=request, format=format),
        'revisions': reverse('lyricrevision-list', request=request, format=format),
        'search': reverse('song-search', request=request, format=format),
    })


class ArtistListView(ListView):
    model = Artist

    def get_context_data(self, **kwargs):
        context = super(ArtistListView, self).get_context_data(**kwargs)
        context['form'] = ArtistForm()
        return context


class ArtistDetailView(DetailView):
    model = Artist
    queryset = Artist.objects.prefetch_related('albums')


class AlbumDetailView(DetailView):
    model = Album
    queryset = Album.objects.prefetch_related('songs')


class SongDetailView(DetailView):
    model = Song


class SearchView(ListView):
    model = Song

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        if not query:
            queryset = Song.objects.none()
        else:
            parts = query.split(' ')
            q = Q()
            for part in parts:
                q = q & (Q(title__icontains=part) | Q(album__title__icontains=part)
                         | Q(album__artist__name__icontains=part))
            queryset = Song.objects.filter(q)

        return queryset


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
