from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from music.models import Song


def save_file_to_firebase(file, album_name):
    from ..views import FB_C
    audio_file_folder = 'music/song/'+album_name+'/'
    firebase = FB_C().get_firebase_instance()
    storage = firebase.storage()
    storage.child(audio_file_folder + str(file)).put(file)
    file_url = storage.child(audio_file_folder + str(file)).get_url(None)
    return file_url

def get_song_list(request):
    songs = Song.objects.all()
    context = {
        'songs': songs,
        'title': 'All songs'
    }
    return render(request, 'music/song/song_list.html', context)

def make_song(request, album_id):
    from ..views import album_details
    from ..models import Album
    is_form_valid = True
    audio_file = None
    error_msg = []
    if request.method == 'POST':
        song_title = request.POST['song_title']
        if not song_title:
            error_msg.append('Title required')
            is_form_valid = False
        if not request.FILES:
            error_msg.append('Upload a file')
            is_form_valid = False
        else:
            if not (request.FILES['song_file'].content_type).__contains__('audio/'):
                error_msg.append('Upload an audio file')
                is_form_valid = False
            else:
                audio_file = request.FILES['song_file']

        print(error_msg)
        if(is_form_valid):
            current_album = Album.objects.get(pk=album_id)
            audio_file = save_file_to_firebase(audio_file, current_album.album_title+str(album_id))
            song = Song(song_title=song_title, album=current_album, file_url=audio_file)
            song.save()
            return album_details(request, album_id)
        album = get_object_or_404(Album, pk=album_id)
        songs = album.song_set.all()
        context = {
            'title': album.album_title,
            'album': album,
            'songs': songs,
            'error_msg': error_msg,
        }
        return render(request, 'music/album/details.html', context)
    else:
        return album_details(request, album_id)
