from pyrebase import pyrebase


class FB_C:
    config = {
        'apiKey': "AIzaSyBnmaZaBEOclGeVeJHygiTMvSvc6v2BWMg",
        'authDomain': "theoryofcreativity-4241e.firebaseapp.com",
        'databaseURL': "https://theoryofcreativity-4241e.firebaseio.com",
        'projectId': "theoryofcreativity-4241e",
        'storageBucket': "theoryofcreativity-4241e.appspot.com",
        'messagingSenderId': "789207444088",
        #firebase configs here
    }
    config_a = {
        'apiKey': "AIzaSyBnmaZaBEOclGeVeJHygiTMvSvc6v2BWMg",
        'authDomain': "theoryofcreativity-4241e.firebaseapp.com",
        'databaseURL': "https://theoryofcreativity-4241e.firebaseio.com",
        'projectId': "theoryofcreativity-4241e",
        'storageBucket': "theoryofcreativity-4241e.appspot.com",
        'messagingSenderId': "789207444088",
        "serviceAccount": 'theoryofcreativity-4241e-firebase-adminsdk-94vcb-f88eb91eb9.json'
        #firebase admin configs here
    }

    def get_firebase_instance(self, **kwargs):
        if kwargs:
            if kwargs['type']=='admin':
                return pyrebase.initialize_app(self.config_a)
        else:
            return pyrebase.initialize_app(self.config)