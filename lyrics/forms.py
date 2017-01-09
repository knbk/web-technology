from django import forms

from .models import Artist, Album, Song, LyricRevision


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ('name', 'bio')


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('artist', 'title')
        widgets = {
            'artist': forms.HiddenInput(),
        }


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('album', 'title')
