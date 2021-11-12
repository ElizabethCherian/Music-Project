from django.db import models
from django.db.models import fields
from django.forms.widgets import NumberInput
from Music.models import Album
from django import forms
import datetime



class Albumform(forms.Form):
    artist=forms.CharField(max_length=50)
    album_title=forms.CharField(max_length=50)
    genre=forms.CharField(max_length=50)
    album_logo=forms.FileField()