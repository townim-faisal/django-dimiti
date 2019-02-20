from django.contrib import admin

# Register your models here.
from music.models import Album, Song, File_type

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(File_type)