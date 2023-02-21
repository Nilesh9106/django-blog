from django.shortcuts import render,redirect
from home.models import *
from home.forms import *
# Create your views here.
def HomeView(request):
    blogs = Blog.objects.filter(status='2')
    return render(request,'home/home.html',{"blogs":blogs}) 

def AboutView(request):
    
    return render(request,'home/about.html')

def ContactView(request):
    
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

def dasshbordView(request):
    if request.user.is_authenticated == False:
        return redirect('home')

    return render(request,'home/dashboard.html')