from django.utils.text import slugify

from rest_framework import serializers
from lyrics.models import Artist, Album, Song, LyricRevision


class ArtistSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Artist
        fields = ('id', 'name', 'slug', 'bio')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super(ArtistSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['name'])
        return super(ArtistSerializer, self).update(instance, validated_data)


class AlbumSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Album
        fields = ('id', 'title', 'slug', 'artist')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super(AlbumSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super(AlbumSerializer, self).update(instance, validated_data)


class SongSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Song
        fields = ('id', 'title', 'slug', 'album')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super(SongSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super(SongSerializer, self).update(instance, validated_data)
