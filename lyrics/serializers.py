from django.utils.text import slugify

from rest_framework import serializers
from lyrics.models import Artist, Album, Song, LyricRevision


class ArtistSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.ReadOnlyField()
    albums = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='album-detail')

    class Meta:
        model = Artist
        fields = ('url', 'id', 'name', 'slug', 'bio', 'albums')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super(ArtistSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super(ArtistSerializer, self).update(instance, validated_data)


class AlbumSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Album
        fields = ('url', 'id', 'title', 'slug', 'artist')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super(AlbumSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super(AlbumSerializer, self).update(instance, validated_data)


class SongSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Song
        fields = ('url', 'id', 'title', 'slug', 'album')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super(SongSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super(SongSerializer, self).update(instance, validated_data)
