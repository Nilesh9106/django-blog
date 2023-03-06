from django.shortcuts import render
from taggit.models import Tag
from home.models import *
# Create your views here.

def tagView(request,tag):
    posts = Blog.objects.filter(tags__name__in=[tag],status='2')
    return render(request,'tag/tag.html',{'posts':posts,'tag':tag})