
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL


# Create your models here.


class Album(models.Model):
    artist=models.CharField(max_length=40)
    album_title=models.CharField(max_length=200)
    genre=models.CharField(max_length=100)
    album_logo=models.FileField(upload_to="AlbumCover/",null=True)

    def __str__(self):
        return f"{self.artist}-{self.album_title}-{self.album_logo}"
        

class Song(models.Model):
    album=models.ForeignKey(Album,on_delete=models.CASCADE)
    file_type=models.CharField(max_length=20)
    song_title=models.CharField(max_length=200)
    audio=models.FileField(upload_to="Audios/",null=True)
    

    def __str__(self):
        return self.song_title+"-"+self.file_type

class FavSongs(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    song=models.ForeignKey(Song,on_delete=models.SET_NULL,null=True)
    song_album=models.ForeignKey(Album,on_delete=models.SET_NULL,null=True)
   