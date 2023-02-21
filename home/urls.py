from django.urls import path,include
from .views import *
urlpatterns = [
    path('',HomeView,name='home'),
    path('about/',AboutView,name='about'),
    path('contact/',ContactView,name='contact'),
    path('search/',SearchView,name='search'),
    path('dashboard/',dasshbordView,name='dashboard'),
    path('@<str:user>/',profileView,name='profile'),
]
