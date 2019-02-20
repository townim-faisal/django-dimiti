from django.db import models

# Create your models here.

class Album(models.Model):
    album_title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    image = models.CharField(max_length=300, blank=True, null=True)
    class Meta:
        ordering = ['album_title']

    def __str__(self):
        return self.album_title+" - "+self.artist

class File_type(models.Model):
    f_type = models.CharField(max_length=10)

    def __str__(self):
        return self.f_type

class Song(models.Model):
    song_title = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    file_url = models.CharField(max_length=500)

    class Meta:
        ordering = ['song_title']
    def __str__(self):
        return self.song_title