from django.shortcuts import render,redirect
from home.models import *
from home.forms import *
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.
def HomeView(request):
    blogs = Blog.objects.filter(status='2').order_by('-created_at')
    paginator = Paginator(blogs, 12) 
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request,'home/home.html',{"blogs":blogs}) 

def AboutView(request):
    
    return render(request,'home/about.html')

def ContactView(request):
    
    if request.method == "POST":
        email = request.POST.get('email')
        name = request.POST.get('name')
        message = request.POST.get('message')
        contact = Contact(email=email,name=name,message=message)
        contact.save()
        messages.success(request,"Message Sent successfully !!")
    
    return render(request,'home/contact.html')

def SearchView(request):
    if request.GET.get('query') is not None:
        search= request.GET.get('query')
        blogs1 = Blog.objects.filter(status='2',title__icontains=search)
        blogs2 = Blog.objects.filter(status='2',description__icontains=search)
        blogs=blogs1.union(blogs2)
    else:
        blogs={}

    return render(request,'home/search.html',{"blogs":blogs})

def profileView(request,user):
    user = User.objects.filter(username=user).first()
    profile = UserProfile.objects.filter(user=user).first()
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/@'+user.username)
    form = ProfileForm(instance=profile)
    blogs=Blog.objects.filter(user=profile,status='2')
    comments=Comment.objects.filter(user=profile).count()
    subscribers= Subscriber.objects.filter(user=profile).count()
    return render(request,'home/profile.html',{'profile':profile,'form':form,'blogs':blogs,'comments':comments,'subscribers':subscribers})
