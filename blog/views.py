import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from home.models import Blog,Comment,UserProfile
from .forms import PostForm
from django.contrib import messages
# Create your views here.

def CreateView(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            slug=form.cleaned_data['slug'] 
            post = form.save(commit=False)
            post.user = UserProfile.objects.filter(user=request.user).first()
            slug=slug.strip().lower()
            post.slug=slug.replace(" ","-")
            post.save()
            form.save_m2m()
            return redirect('/blog/'+request.user.username+'/'+post.slug)

    form = PostForm()
    return render(request,'blog/create.html',{'form':form})
    

def UpdateView(request,user,slug):
    user = User.objects.filter(username=user).first()
    user= UserProfile.objects.filter(user=user).first()
    post2 = Blog.objects.filter(user=user,slug=slug).first()

    if request.user.is_authenticated and user.user.username == request.user.username:    
        if request.method == 'POST' :
            form = PostForm(request.POST,request.FILES,instance=post2)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                form.save_m2m()
                return redirect('/blog/'+user.user.username+'/'+post2.slug)
        else:
            form = PostForm(instance=post2)
            return render(request,'blog/create.html',{'form':form})
    else:
        
        messages.error(request,'you are not allow to update this blog')
        return redirect('/')

def DeleteView(request,user,slug):
    user = User.objects.filter(username=user).first()
    user = UserProfile.objects.filter(user=user).first()
    post= Blog.objects.filter(user=user,slug=slug).first()

    if request.user.is_authenticated and user.user.username == request.user.username:
        post.delete()
        messages.warning(request,message="Your Blog is deleted !!!")    
        return redirect('home')
    else:
        messages.error(request,message="You does not have permission to delete blog !!")
        return redirect('home')


def subsite(request,user):
    if User.objects.filter(username=user).exists():
        site = User.objects.filter(username=user).first()
        site = UserProfile.objects.filter(user=site).first()
        blogs = Blog.objects.filter(user=site,status='2')
        return render(request,'blog/site.html',{'site':site,"blogs":blogs})
    else:
        return render(request,'404.html')

def subsiteBlog(request,user,slug):

    if User.objects.filter(username=user).exists():
        site1 = User.objects.filter(username=user).first()
        site = UserProfile.objects.filter(user=site1).first()

        if Blog.objects.filter(user=site,slug=slug).exists():
            blog = Blog.objects.filter(user=site,slug=slug)[0]
            if blog.status == '1' and request.user != site1:
                return render(request,'404.html')
            tags = blog.tags.names()
            body = blog.body
            comments = Comment.objects.filter(post=blog,parent=None).order_by('created_at')
            replies = Comment.objects.filter(post=blog).exclude(parent=None)
            profile= UserProfile.objects.filter(user=site1).first()

            # arranging reply with comments
            repDict ={}
            for reply in replies:
                if reply.parent.id not in repDict.keys():
                    repDict[reply.parent.id] = [reply]
                else:
                    repDict[reply.parent.id].append(reply)
            
            return render(request,'blog/blog.html',{'blog':blog,'tags':tags,'body':body,'comments':comments,'replies':repDict,'profile':profile})
        else:
            return render(request,'404.html')
        
    else:
        return render(request,'404.html')


def CommentView(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        username = request.POST.get('username')
        if request.user.is_authenticated:
            commentBody = request.POST.get('comment')
            user = User.objects.filter(username=username).first()
            profile = UserProfile.objects.filter(user=user).first()
            profileComm = UserProfile.objects.filter(user=request.user).first()
            parent = request.POST.get('parent')
            post = Blog.objects.filter(slug=slug,user=profile).first()
            
            if parent == '':
                comm = Comment(commentBody=commentBody,user=profileComm,post=post)
            else:
                P = Comment.objects.filter(id=parent).first()
                comm = Comment(commentBody=commentBody,user=profileComm,post=post,parent=P)
            comm.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            messages.error(request,'you are not logged in')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return redirect('home')


def DeleteCommentView(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        id = data['id']
        if(id != None):
            Comment.objects.filter(id = id).delete()
            return JsonResponse({"msg":"success"})
        else:
            return JsonResponse({"msg":"error"})


def draftBlogView(request):
    user = request.user
    if(request.user.is_authenticated == False):
        return redirect('login')
    profile = UserProfile.objects.filter(user=user).first()

    blogs = Blog.objects.filter(user=profile,status='1')

    return render(request,'blog/drafts.html',{"blogs":blogs})
