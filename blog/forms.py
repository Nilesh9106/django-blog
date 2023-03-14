from home.models import *
from django import forms 
from tinymce.models import HTMLField
from taggit.forms import *

class PostForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput,required=False)
    class Meta:
        model = Blog
        fields = ["slug", "title", "description", "tags",'status',"image","body"]

class ReportForm(forms.ModelForm):

    class Meta:
        model=Report
        fields=['report']