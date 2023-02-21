
from django.urls import path
from tag.views import *
urlpatterns = [
    path('<str:tag>/',tagView,name='tag'),
]
