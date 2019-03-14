
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from music.models import Song
from music.others.firebase_crud import save_file_to_firebase, delete_from_firebase
from music.song.lyric_finder import parse_lyric


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

        #print(error_msg)
        if(is_form_valid):
            current_album = Album.objects.get(pk=album_id)
            lyric = parse_lyric(song_title, current_album.artist)
            audio_file = save_file_to_firebase(file=audio_file, type='audio', path=current_album.album_title+str(album_id))
            file_url = audio_file[0]
            file_path = audio_file[1]
            song = Song(song_title=song_title, album=current_album, file_url=file_url, file_path=file_path, lyrics = lyric)
            song.save()
            return HttpResponseRedirect(reverse('music:album-details', args=(album_id,)))
        album = get_object_or_404(Album, pk=album_id)
        songs = album.song_set.all()
        context = {
            'title': album.album_title,
            'album': album,
            'songs': songs,
            'error_msg': error_msg,
        }
        return album_details(request, album_id, context = context)
        #return render(request, 'music/album/details.html', context)
    else:
        #return album_details(request, album_id)
        return HttpResponseRedirect(reverse('music:album-details', args=(album_id,)))


def remove_song(request, album_id, song_id):
    from ..views import album_details, song_list
    song = get_object_or_404(Song, id=song_id)
    delete_from_firebase(song.file_path)
    song.delete()
    if album_id:
        #return album_details(request, album_id)
        return HttpResponseRedirect(reverse('music:album-details', args=(album_id,)))
    else:
        #return song_list(request)
        return HttpResponseRedirect(reverse('music:song-list'))
