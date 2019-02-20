from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from pyrebase import pyrebase

from music.models import Album

album_cover_folder = 'music/album_cover/'

def get_album_list(request):
    albums = Album.objects.all()
    context = {
        'title': 'song list',
        'albums': albums,
    }
    return render(request, 'music/album/album_list.html', context)

def get_album_details(request, album_id, **kwargs):
    album = get_object_or_404(Album, pk=album_id)
    songs = album.song_set.all()
    context = {
        'title': album.album_title,
        'album': album,
        'songs': songs
    }
    return render(request, 'music/album/details.html', context)


def save_img_to_firebase(img):
    from ..views import FB_C
    firebase = FB_C().get_firebase_instance()
    storage = firebase.storage()
    storage.child(album_cover_folder + str(img)).put(img)
    im_url = storage.child(album_cover_folder + str(img)).get_url(None)
    return im_url


def make_album(request):
    error_msg = []
    context = {
        'title': 'Create Album',
        'error_msg': error_msg,
    }
    if request.method == 'GET':
        print(request.method)
        return render(request, 'music/album/create_album.html', context)

    else:
        is_form_valid = True
        print(request.POST)
        album_title = request.POST['album_title']
        artist = request.POST['artist']
        img = None
        if request.FILES and (not request.FILES['album_cover'].content_type.__contains__('image/')): #check valid file
            context['error_msg'].append('Upload an image file')
            is_form_valid = False
        elif request.FILES and request.FILES['album_cover'].content_type.__contains__('image/'):
            img = request.FILES['album_cover']

        if not (album_title and artist): #check all fields filled
            context['error_msg'].append('Fill up all fields')
            is_form_valid = False

        if is_form_valid:
            if img:
                img = save_img_to_firebase(img)
            album = Album(album_title=album_title, artist=artist, image=img)
            album.save()
            return get_album_details(request, album.id)
        return render(request, 'music/album/create_album.html', context)