from django.contrib import admin
from django.urls import path
from Music import views


urlpatterns = [
   
    path('',views.Albumdisplay,name="index"),
    path('details/<int:albid>',views.Albumdetails,name="details"),
    path('favorite/<int:songid>',views.FavouriteSong,name="favorite"),
    path('unfavorite/<int:songid>',views.UnFavouriteSong,name="unfavorite"),
    path('addsong/<int:albid>',views.AddSong,name="add-song"),
    path('delete/<int:albid>',views.DeleteAlbum,name="delete"),
    path('addalbum/',views.AddAlbum1,name="addalbum"),
    path('updatealbum/<int:albid>',views.UpdateAlbum,name="album-update"),
    path('songs/',views.Songs,name="songs"),
    path('deletesong/<int:songid>',views.DeleteSong,name="delete-song"),
    path('updatesong/<int:songid>',views.UpdateSong,name="update-song"),
    path('search/',views.Search,name="search"),
    path('registration/',views.register,name="register"),
    path('login/',views.Login,name="login"),
    path('logout/',views.Logout,name="logout"),
]