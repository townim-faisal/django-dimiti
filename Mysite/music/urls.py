"""Mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from music import views

app_name = 'music'

urlpatterns = [
    re_path(r'^$', views.album_list, name='album-list'),
    path('<int:album_id>/', views.album_details, name='album-details'),
    path('all-songs/', views.song_list, name='song-list'),
    path('create_album/', views.create_album, name='create-album'),
    path('create_song/<int:album_id>/', views.create_song, name='create-song'),
    path('delete_album/<int:album_id>/', views.delete_album, name='delete-album'),
    path('delete_song/<int:album_id>/<int:song_id>/', views.delete_song, name='delete-song-fa'),
    path('delete_song/<int:song_id>/', views.delete_song, name='delete-song'),
]
