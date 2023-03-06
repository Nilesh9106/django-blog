from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .forms import *
from django.contrib.auth.decorators import login_required
from home.models import *
# Create your views here.
@login_required
def dashboardView(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    posts = Blog.objects.filter(user=profile,status='2').order_by('-updated_at')
    subscribers = Subscriber.objects.filter(user=profile)
    count= posts.count()
    
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request,'dashboard/home.html',{"profile":profile,'posts':posts,"subscribers":subscribers,"count":count})

@login_required
def draftsView(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    posts = Blog.objects.filter(user=profile,status='1').order_by('-created_at')
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request,'dashboard/drafts.html',{"profile":profile,'posts':posts})

@login_required
def subscribersView(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    subscribers = Subscriber.objects.filter(user=profile).order_by('-created_at')
    paginator = Paginator(subscribers, 10) 
    page_number = request.GET.get('page')
    subscribers = paginator.get_page(page_number)
    return render(request,'dashboard/subscribers.html',{"subscribers":subscribers})

@login_required
def seoView(request):
    profile = UserProfile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = SeoForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
    
    form=SeoForm(instance=profile)
    return render(request,'dashboard/seo.html',{"form":form})