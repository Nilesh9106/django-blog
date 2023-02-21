from home.models import Blog
from django import forms 
from tinymce.models import HTMLField
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):

    class Meta:
        model= User
        fields = ('username','first_name','last_name','email','password1','password2')
        widgets = {
            'username':forms.TextInput(attrs={
                'class':"w-full bg-white rounded border border-gray-300 focus:border-green-500 dark:text-gray-50 dark:bg-gray-600 dark:focus:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-green-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
            }),
            'first_name':forms.TextInput(attrs={
                'class':"w-full bg-white rounded border border-gray-300 focus:border-green-500 dark:text-gray-50 dark:bg-gray-600 dark:focus:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-green-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
            }),
            'last_name':forms.TextInput(attrs={
                'class':"w-full bg-white rounded border border-gray-300 focus:border-green-500 dark:text-gray-50 dark:bg-gray-600 dark:focus:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-green-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
            }),
            'email':forms.EmailInput(attrs={
                'class':"w-full bg-white rounded border border-gray-300 focus:border-green-500 dark:text-gray-50 dark:bg-gray-600 dark:focus:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-green-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out"
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['class'] = 'w-full bg-white rounded border border-gray-300 focus:border-green-500 dark:text-gray-50 dark:bg-gray-600 dark:focus:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-green-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out'
        self.fields['password2'].widget.attrs['class'] = 'w-full bg-white rounded border border-gray-300 focus:border-green-500 dark:text-gray-50 dark:bg-gray-600 dark:focus:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-green-200 text-base outline-none text-gray-700 py-1 px-3 leading-8 transition-colors duration-200 ease-in-out'

class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['password'].widget.attrs['class'] = 'input'
