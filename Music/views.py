from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from Music.models import Album,Song,FavSongs
from .forms import Albumform
from django.contrib import auth
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,unauthenticated_user
from django.db.models import Q

# Create your views here.

def Albumdisplay(request):
    all_album=Album.objects.all()
    return render(request,"Music/home.html",{'albums':all_album})

@login_required(login_url='/music/login/')
def Albumdetails(request,albid):
    this_album=Album.objects.get(id=albid)
    request.session["albid"]=albid
    flag=0
    if request.method=='POST':
        flag=1
        fav=FavSongs.objects.filter(user=request.user,song_album=this_album).count()
        if fav>0:
            s=1
            favorite=list(FavSongs.objects.filter(user=request.user,song_album=this_album))
         
            return render(request,"Music/dtls.html",{"album":this_album,"flag":flag,"favorite":favorite,"s":s})
        else:
            s=0
            
            return render(request,"Music/dtls.html",{"album":this_album,"flag":flag,"s":s})
    else:
        return render(request,"Music/dtls.html",{"album":this_album,"flag":flag})

    
   

@login_required(login_url='/music/login/')
def FavouriteSong(request,songid):
    this_album=Album.objects.get(id=request.session["albid"])
    selected_song=this_album.song_set.get(id=songid)
    
    flag=1
    f=FavSongs.objects.filter(user=request.user,song=songid).count()
    if f==0:
        FavSongs.objects.create(user=request.user,song=selected_song,song_album=this_album)
    
    s=1
    
    favorite=list(FavSongs.objects.filter(user=request.user,song_album=this_album))
        
    return render(request,"Music/dtls.html",{"album":this_album,"flag":flag,"favorite":favorite,"s":s})
    
    

@login_required(login_url='/music/login/')
def UnFavouriteSong(request,songid):
    this_album=Album.objects.get(id=request.session["albid"])
    selected_song=this_album.song_set.get(id=songid)
    record=FavSongs.objects.get(user=request.user,song=songid)
    record.delete()

    flag=1
    fav=FavSongs.objects.filter(user=request.user,song_album=this_album).count()
    if fav>0:
        s=1
        favorite=list(FavSongs.objects.filter(user=request.user,song_album=this_album))
        return render(request,"Music/dtls.html",{"album":this_album,"flag":flag,"favorite":favorite,"s":s})
    else:
        s=0
            
        return render(request,"Music/dtls.html",{"album":this_album,"flag":flag,'s':s})
    


@login_required(login_url='/music/login/')
@allowed_users(allowed_roles=['admin'])
def AddSong(request,albid):
    albobj=Album.objects.get(id=albid)

    if request.method=='POST'and request.FILES:
            
        Song.objects.create(album=albobj,file_type=request.POST.get("filetype"),song_title=request.POST.get("songtitle"),
                                audio=request.FILES.get("audio"))
       
        return render(request,"Music/dtls.html",{"album":albobj})
    else:
        return render(request,"Music/AddSong.html")
    
    



@login_required(login_url='/music/login/')
@allowed_users(allowed_roles=['admin'])
def DeleteAlbum(request,albid):
    all_album=Album.objects.all()
    
    select_album=Album.objects.get(id=albid)
    select_album.delete()
        
    return render(request,"Music/home.html",{'albums':all_album})
    
    

@login_required(login_url='/music/login/')
@allowed_users(allowed_roles=['admin'])
def AddAlbum1(request):
    
    if request.method=='POST' and request.FILES:
        artst=request.POST.get("artist")
        title=request.POST.get("album_title")
        gnr=request.POST.get("genre")
        logo=request.FILES.get("album_logo")
        Album.objects.create(artist=artst,album_title=title,genre=gnr,album_logo=logo)
        return redirect('/music/index/')
            
    else:
        return render(request,"Music/AddAlbum.html")
    



@login_required(login_url='/music/login/')
@allowed_users(allowed_roles=['admin'])
def UpdateAlbum(request,albid):
    
    select_album=Album.objects.get(id=albid)
    if request.method=='POST' or request.FILES:
        select_album.artist=request.POST.get("artist")
        select_album.album_title=request.POST.get("album_title")
        select_album.genre=request.POST.get("genre")
        if request.FILES:
            select_album.album_logo=request.FILES.get("album_logo")
        select_album.save()
        return render(request,"Music/dtls.html",{"album":select_album})
    else:
        return render(request,"Music/Updatealbum.html",{"album":select_album})
    


def Songs(request):
    song_record=Song.objects.all()
   
    return render(request,"Music/Songs.html",{'songs':song_record})


@login_required(login_url='/music/login/')
@allowed_users(allowed_roles=['admin'])
def DeleteSong(request,songid):
    
    select_song=Song.objects.get(id=songid)
    select_song.delete()
    all_songs=Song.objects.all()
    return render(request,"Music/Songs.html",{'songs':all_songs})
    



@login_required(login_url='/music/login/')
@allowed_users(allowed_roles=['admin'])
def UpdateSong(request,songid):
    
    select_song=Song.objects.get(id=songid)
    if request.method=='POST':
        
        select_song.song_title=request.POST.get("song_title")
        select_song.file_type=request.POST.get("file_type")
        select_song.save()
        all_songs=Song.objects.all()
        return render(request,"Music/Songs.html",{"songs":all_songs})
    else:
        return render(request,"Music/Updatesong.html",{"song":select_song})
    

        
def Search(request):
    if request.method=='POST':
        search_item=request.POST.get("search")

        albumlist=Album.objects.filter(Q(album_title__icontains=search_item) | Q(genre__icontains=search_item) | Q(artist__icontains=search_item))
        song=Song.objects.filter(Q(song_title__icontains=search_item) | Q(file_type__icontains=search_item))

        if albumlist:
            return render(request,"Music/search.html",{'album':albumlist})
        elif song:
            return render(request,"Music/search.html",{'song':song})
        
        else:
            return render(request,"Music/search.html",{'err':"No items matching"})
    else:
        return render(request,"Music/home.html")


@unauthenticated_user
def register(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/music/login/')
        else:
            print(form.errors)
            return HttpResponse("form not valid")
    else:
        return render(request,"Music/Register.html",{'form':form})


@unauthenticated_user
def Login(request):
    if request.method=='POST':
        user=auth.authenticate(request,username=request.POST["txtUsername"],password=request.POST["txtPassword"])
        
        if user is not None:
            if request.GET.get('next'):
                auth.login(request,user)
                return redirect(request.GET.get('next'))
            else:
                auth.login(request,user)
                return redirect('/music/')
            
        else:
            return render(request,"Music/Login.html",{"errors":'Invalid Login credentials!!!'})
    else:
        return render(request,"Music/Login.html")

def Logout(request):
    auth.logout(request)
    return redirect('/music/')
