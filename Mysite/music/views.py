from .albums.album_crud import *
from .song.song_crud import *
import pyrebase;

from django.contrib.auth.decorators import login_required
# Create your views here.
##Firebase



##

@login_required()
def album_list(request):
    return get_album_list(request)

@login_required()
def album_details(request, album_id, **kwargs):
    return get_album_details(request, album_id, **kwargs)

@login_required()
def song_list(request):
    return get_song_list(request)

@login_required()
def create_album(request):
    return make_album(request)

@login_required()
def create_song(request, album_id):
    return make_song(request, album_id)

@login_required()
def delete_song(request, album_id=None, song_id=None):
    return remove_song(request, album_id, song_id)

@login_required()
def delete_album(request, album_id):
    return remove_album(request, album_id)
