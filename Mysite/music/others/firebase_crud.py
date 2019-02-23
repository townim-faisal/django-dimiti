from datetime import datetime
from pyrebase import pyrebase


class FB_C:
    config = {
        #firebase configs here
    }
    config_a = {
        #firebase admin configs here
    }

    def get_firebase_instance(self, **kwargs):
        if kwargs:
            if kwargs['type']=='admin':
                return pyrebase.initialize_app(self.config_a)
        else:
            return pyrebase.initialize_app(self.config)



def save_file_to_firebase(**kwargs):
    firebase = FB_C().get_firebase_instance()
    storage = firebase.storage()
    if kwargs:
        file = kwargs['file']
        album_name = kwargs['album_name']
        file_path = ''

        if kwargs['type']=='image':
            file_path = 'album_covers/' + album_name + str(datetime.now()) + '/' + str(file)

        elif kwargs['type']=='audio':
            file_path = 'music/song/' + album_name + '/'+ str(file)

        storage.child(file_path).put(file)
        file_url = storage.child(file_path).get_url(None)
        return [file_url, file_path]


def delete_from_firebase(file_path):
    firebase = FB_C().get_firebase_instance(type='admin')
    storage = firebase.storage()
    storage.delete(file_path)
