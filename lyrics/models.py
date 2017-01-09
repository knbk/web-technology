from __future__ import unicode_literals

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db import transaction
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible


class NaturalKeyManager(models.Manager):
    def __init__(self, field='slug', *args, **kwargs):
        super(NaturalKeyManager, self).__init__(*args, **kwargs)
        self.field = field

    def get_by_natural_key(self, key):
        return self.get(**{self.field: key})


@python_2_unicode_compatible
class Artist(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    bio = models.TextField(blank=True)

    objects = NaturalKeyManager('slug')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT, related_name='albums')
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    objects = NaturalKeyManager('slug')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.PROTECT, related_name='songs')
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    @property
    def lyrics(self):
        revision = self.get_current_revision()
        return revision.lyrics if revision else ''

    def create_revision(self, lyrics, editor=None):
        with transaction.atomic():
            # Acquire lock and add new revision to tail of linked list
            tail = self.get_current_revision()
            revision = self.revisions.create(song=self, lyrics=lyrics, editor=editor, previous=tail)
        return revision

    def rollback_to_revision(self, revision):
        if not isinstance(revision, LyricRevision):
            revision = LyricRevision.objects.get(pk=revision)

        if revision.song != self:
            raise ValueError('')

    def get_current_revision(self):
        try:
            return self.revisions.get(next=None)
        except ObjectDoesNotExist:
            return None

    objects = NaturalKeyManager('slug')

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class LyricRevision(models.Model):
    song = models.ForeignKey(Song, on_delete=models.PROTECT, related_name='revisions')
    previous = models.OneToOneField('self', on_delete=models.PROTECT, related_name='next', null=True)

    editor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='edits', null=True)
    created_at = models.DateTimeField(default=timezone.now)

    lyrics = models.TextField(blank=True)

    def __str__(self):
        return self.song.title
