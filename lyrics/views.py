from django.shortcuts import render
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from lyrics.models import Artist
from lyrics.serializers import ArtistSerializer


def home(request):
    return render(request, 'home.html')


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'artists': reverse('artist-list', request=request, format=format),
    })


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
