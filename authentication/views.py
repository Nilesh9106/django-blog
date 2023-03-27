from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from home.models import *
from verify_email.email_handler import send_verification_email
from django.core.mail import EmailMessage
from django.conf import settings
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
            inactive_user = send_verification_email(request, form)

            messages.success(request,'your account created successfully. login to your account')
            return redirect('login')
    
    form = SignupForm()
    return render(request,'auth/signup.html',{'form':form})

def LogoutView(request):
    messages.success(request,'you logout successfully')
    logout(request)
    return redirect('home')

def Subscribe(request):
    if request.GET.get("email"):
        email = request.GET.get("email")
        user = request.GET.get("user")
        code = request.GET.get("code")
        user = User.objects.filter(username=user).first()
        user = UserProfile.objects.filter(user=user).first()
        # print(1)
        if email is None or user is None or code is None:
            return render(request, '404.html')
        
        if Subscriber.objects.filter(email=email,user=user).exists() and Subscriber.objects.filter(email=email,user=user).first().status == '2':
            # print(2)
            messages.error(request,f"{email} is already verified")
            return redirect("home")
        elif Subscriber.objects.filter(email=email,user=user).exists():
            sub = Subscriber.objects.filter(email=email,user=user).first()
            if sub.code == code:
                sub.status = '2'
                sub.save()
                messages.success(request,f"you subscribed to {user.user.username} successfully")
            else:
                messages.error(request,f"Wrong URL Provided")
            return redirect("home")
        else:
            messages.error(request,f"{email} is not subscribed to {user.user.username} ")
            return redirect("home")
           