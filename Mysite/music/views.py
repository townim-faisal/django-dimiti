from .albums.album_crud import *
from .song.song_crud import *
import pyrebase;
# Create your views here.
##Firebase

class FB_C:
    config = {
        'apiKey': "AIzaSyBnmaZaBEOclGeVeJHygiTMvSvc6v2BWMg",
        'authDomain': "theoryofcreativity-4241e.firebaseapp.com",
        'databaseURL': "https://theoryofcreativity-4241e.firebaseio.com",
        'projectId': "theoryofcreativity-4241e",
        'storageBucket': "theoryofcreativity-4241e.appspot.com",
        'messagingSenderId': "789207444088"
    }
    def get_firebase_instance(self):
        return pyrebase.initialize_app(self.config)


##


def album_list(request):
    return get_album_list(request)


def album_details(request, album_id):
    return get_album_details(request, album_id)


def song_list(request):
    return get_song_list(request)


def create_album(request):
    return make_album(request)

def create_song(request, album_id):
    return make_song(request, album_id)