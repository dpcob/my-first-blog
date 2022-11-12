# from socket import fromshare
from django import forms

from .models import Post, Simg

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ("title","thumb","text",)

class SimgForm(forms.ModelForm):
    
    class Meta:
        model = Simg
        fields = ("imgf",)