from django.forms import *
from home.models import *

class SeoForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=['about','siteTitle','siteDescription','siteImage']
        