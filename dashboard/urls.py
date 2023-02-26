from django.urls import path,include
from .views import *
urlpatterns = [
    path('',dashboardView ,name='dashboard'),
    path('drafts/',draftsView ,name='draftDashboard'),
    path('subscribers/',subscribersView ,name='subscribers'),
    path('seo/',seoView,name='seo'),
]
