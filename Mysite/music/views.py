from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from music.models import Album, Song


# Create your views here.
def album_list(request):
    albums = Album.objects.all()
    context = {
        'title': 'song list',
        'albums': albums,
    }
    return render(request, 'music/album_list.html', context)

def album_details(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    songs = album.song_set.all()
    context = {
        'title': album.album_title,
        'album': album,
        'songs': songs
    }
    return render(request, 'music/details.html', context)


def song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs,
        'title': 'All songs'
    }
    return render(request, 'music/song_list.html', context)