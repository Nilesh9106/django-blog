from home.models import Blog
from django import forms 
from tinymce.models import HTMLField
from taggit.forms import *

class PostForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput,required=False)
    class Meta:
        model = Blog
        fields = ["slug", "title", "description", "tags",'status',"image","body"]