from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db import transaction
from django.utils import timezone


class NaturalKeyManager(models.Manager):
    def __init__(self, field, *args, **kwargs):
        super(NaturalKeyManager, self).__init__(*args, **kwargs)
        self.field = field

    def get_by_natural_key(self, key):
        return self.get(**{self.field: key})


class Artist(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    bio = models.TextField(blank=True)

    objects = NaturalKeyManager('slug')


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='albums')
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    objects = NaturalKeyManager('slug')


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.PROTECT, related_name='songs')
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    def create_revision(self, lyrics, editor=None):
        with transaction.atomic():
            # Acquire lock and add new revision to tail of linked list
            tail = self.revisions.select_for_update().get(next=None)
            revision = self.revisions.create(song=self, lyrics=lyrics, editor=editor, previous=tail)
        return revision

    def rollback_to_revision(self, revision):
        if not isinstance(revision, LyricRevision):
            revision = LyricRevision.objects.get(pk=revision)

        if revision.song != self:
            raise ValueError('')

    def get_current_revision(self):
        return self.revisions.get(next=None)

    objects = NaturalKeyManager('slug')


class LyricRevision(models.Model):
    song = models.ForeignKey(Song, on_delete=models.PROTECT, related_name='revisions')
    previous = models.OneToOneField('self', on_delete=models.PROTECT, related_name='next', null=True)

    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='edits', null=True)
    created_at = models.DateTimeField(default=timezone.now)

    lyrics = models.TextField(blank=True)
