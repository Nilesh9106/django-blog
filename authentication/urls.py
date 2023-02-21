from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.loginView,name='login'),
    path('signup/',views.signupView,name='signup'),
    path('logout/',views.LogoutView,name='logout'),
]
