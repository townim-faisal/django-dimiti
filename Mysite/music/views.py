from .albums.album_crud import *
from .song.song_crud import *
import pyrebase;
# Create your views here.
##Firebase



##


def album_list(request):
    return get_album_list(request)


def album_details(request, album_id, **kwargs):
    return get_album_details(request, album_id, **kwargs)


def song_list(request):
    return get_song_list(request)


def create_album(request):
    return make_album(request)

def create_song(request, album_id):
    return make_song(request, album_id)

def delete_song(request, album_id=None, song_id=None):
    return remove_song(request, album_id, song_id)


def delete_album(request, album_id):
    return remove_album(request, album_id)