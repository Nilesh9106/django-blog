from django.forms import *
from home.models import *
class ProfileForm(ModelForm):
    profilePic= ImageField(widget=FileInput)
    class Meta:
        model=UserProfile
        fields=['profilePic','about']
        