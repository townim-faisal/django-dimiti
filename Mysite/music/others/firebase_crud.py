from datetime import datetime
from ..config.firebase_config import FB_C

def save_file_to_firebase(**kwargs):
    firebase = FB_C.FB_C().get_firebase_instance()
    storage = firebase.storage()
    if kwargs:
        file = kwargs['file']
        file_path = ''

        if kwargs['type']=='image':
            file_path = kwargs['path'] + str(datetime.now()) + '/' + str(file)

        elif kwargs['type']=='audio':
            file_path = 'music/song/'+kwargs['path']+'/'+str(datetime.now())+ str(file)

        storage.child(file_path).put(file)
        file_url = storage.child(file_path).get_url(None)
        return [file_url, file_path]


def delete_from_firebase(file_path):
    firebase = FB_C.FB_C().get_firebase_instance(type='admin')
    storage = firebase.storage()
    storage.delete(file_path)
