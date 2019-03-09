from .albums.album_crud import *
from .song.song_crud import *
from auth_user.decorators import superuser_required
import pyrebase;

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

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
@superuser_required()
def create_album(request):
    return make_album(request)

@login_required()
@superuser_required()
def create_song(request, album_id):
    return make_song(request, album_id)

@login_required()
def delete_song(request, album_id=None, song_id=None):
    return remove_song(request, album_id, song_id)

@login_required()
@superuser_required()
def delete_album(request, album_id):
    return remove_album(request, album_id)

#user is not superuser
@login_required()
def user_is_not_permitted(request):
    return render(request, 'music/user_not_permitted.html')
