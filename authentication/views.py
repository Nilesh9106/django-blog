from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from home.models import UserProfile
# Create your views here.

def loginView(request):
    if request.user.is_authenticated:
        messages.warning(request,'you already logged in')
        return redirect('/')

    if request.method == 'POST':
        form = LoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
    else:
        form=LoginForm()
    
    return render(request,'auth/login.html',{"form":form})

def signupView(request):
    if request.user.is_authenticated:
        messages.warning(request,'you already logged in')
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            profile = UserProfile(user=user,siteTitle=(user.first_name+"'s Blog"))
            profile.save()
            user.save()
            messages.success(request,'your account created successfully. login to your account')
            return redirect('login')
    
    form = SignupForm()
    return render(request,'auth/signup.html',{'form':form})

def LogoutView(request):
    messages.success(request,'you logout successfully')
    logout(request)
    return redirect('home')