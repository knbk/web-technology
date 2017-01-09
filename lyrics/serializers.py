from django.utils import timezone
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
    songs = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='song-detail')

    class Meta:
        model = Album
        fields = ('url', 'id', 'title', 'slug', 'artist', 'songs')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super(AlbumSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super(AlbumSerializer, self).update(instance, validated_data)


class SongSerializer(serializers.HyperlinkedModelSerializer):
    slug = serializers.ReadOnlyField()
    revisions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='lyricrevision-detail')

    class Meta:
        model = Song
        fields = ('url', 'id', 'title', 'slug', 'album', 'revisions')

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        return super(SongSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'name' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super(SongSerializer, self).update(instance, validated_data)


class LyricSerializer(serializers.HyperlinkedModelSerializer):
    created_at = serializers.ReadOnlyField(default=serializers.CreateOnlyDefault(timezone.now))
    editor = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    previous = serializers.HyperlinkedRelatedField(read_only=True)
    next = serializers.HyperlinkedRelatedField(read_only=True)

    class Meta:
        model = LyricRevision
        fields = ('url', 'id', 'song', 'lyrics', 'created_at', 'editor')

    def create(self, validated_data):
        song = validated_data['song']
        revision = song.create_revision(validated_data['lyrics'], validated_data['editor'])
        return revision

    def update(self, instance, validated_data):
        song = instance.song
        revision = song.create_revision(validated_data['lyrics'], validated_data['editor'])
        return revision
