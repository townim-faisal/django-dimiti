from django.shortcuts import render, get_object_or_404
from music.models import Album
from music.others.firebase_crud import save_file_to_firebase, delete_from_firebase


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
    if kwargs:
        context = kwargs['context']
    #print(context)
    return render(request, 'music/album/details.html', context)


def make_album(request):
    error_msg = []
    context = {
        'title': 'Create Album',
        'error_msg': error_msg,
    }
    if request.method == 'GET':
        #print(request.method)
        return render(request, 'music/album/create_album.html', context)

    else:
        is_form_valid = True
        #print(request.POST)
        album_title = request.POST['album_title']
        artist = request.POST['artist']
        img = None
        file_path = None
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
                img_folder = save_file_to_firebase(file=img, type='image', album_name=album_title)
                img = img_folder[0]
                file_path = img_folder[1]

            album = Album(album_title=album_title, artist=artist, image=img, file_path=file_path)
            album.save()
            return get_album_details(request, album.id)
        return render(request, 'music/album/create_album.html', context)


def remove_album(request, album_id):
    from ..views import album_list
    album = get_object_or_404(Album, id=album_id)
    if album.image and album.file_path:
        delete_from_firebase(album.file_path)
    songs = album.song_set.all()
    for song in songs:
        delete_from_firebase(song.file_path)
        song.delete()
    album.delete()
    return album_list(request)
