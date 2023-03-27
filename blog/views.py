import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from home.models import *
from .forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils.crypto import get_random_string
from django.core.mail import send_mail,EmailMessage
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
            
            if post.status == '2':
                subject = 'New Blog Post'
                head = '''
                    <head>
                        <meta charset="UTF-8">
                        <title>New Blog Post Notification</title>
                        <style>
                        body {
                            font-family: Arial, sans-serif;
                            font-size: 16px;
                            line-height: 1.5;
                            background-color: #f9f9f9;
                            padding: 20px;
                        }
                        .header {
                            text-align: center;
                            margin-bottom: 30px;
                            font-size: 25px;
                        }
                        .title {
                            font-size: 28px;
                            margin-bottom: 20px;
                        }
                        .content {
                            background-color: #fff;
                            border: 1px solid #ccc;
                            border-radius: 5px;
                            padding: 20px;
                            margin-bottom: 30px;
                        }
                        .button {
                            display: inline-block;
                            background-color: #4CAF50;
                            color: #fff;
                            padding: 10px 20px;
                            border-radius: 5px;
                            text-decoration: none;
                            margin-top: 20px;
                        }
                        </style>
                    </head>
                '''
                message = f'''
                    <html>
                        {head}
                    <body>
                        <div class="header">
                        Be A Blogger
                        </div>
                        <div class="content">
                        <h1 class="title">New Blog Post Notification</h1>
                        <p>Dear Subscriber,</p>
                        <p>We are pleased to announce that a new blog post has been uploaded to our website. The post is titled "{post.title}" and you can read it by clicking on the button below:</p>
                        <a href="{settings.DOMAIN}blog/{request.user.username}/{slug}/" class="button">Read Now</a>
                        <p>Thank you for your continued support and we hope you enjoy reading our latest post.</p>
                        <p>Sincerely,</p>
                        <p>Be a Blogger Team</p>
                        </div>
                    </body>
                    </html>
                '''
                email_from = settings.EMAIL_HOST_USER
                subscribers = Subscriber.objects.filter(user=post.user,status='2')

                recipient_list = []
                for sub in subscribers:
                    recipient_list.append(sub.email)

                msg = EmailMessage(subject, message, email_from, recipient_list)
                msg.content_subtype = "html"  # Main content is now text/html
                msg.send()
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
            if request.method == 'POST':
                reportReason = request.POST.get('report')
                report = Report(blog=blog,report=reportReason)
                report.save()
                
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



def subscribeView(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        profile = UserProfile.objects.filter(user=user).first()
        if Subscriber.objects.filter(email=email,user=profile).exists():
            messages.warning(request,f"you already subscribed {username}")
            return redirect('home')
        
        code = get_random_string(length=32)

        subject = 'Subscription Verification'
        message = f'''<p>Dear {email},</p>
    <p>Thank you for subscribing to our newsletter! To ensure that you receive our emails, please click the button below to verify your subscription:</p>
    <a href="{settings.DOMAIN}/auth/subscribe?email={email}&user={username}&code={code}" style="background-color: #008CBA; color: white; display: inline-block; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Subscription</a>
    <p>If you did not sign up for our newsletter, please disregard this email.</p>
    <p>Thank you,</p>
    <p>Be a Blogger Team</p>
'''
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email ]

        msg = EmailMessage(subject, message, email_from, recipient_list)
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        subs = Subscriber(email=email,user=profile,code=code)
        subs.save()
        
        messages.success(request,f"we have sent mail to {email}, please verify your subscription ")
        return redirect('home')
    
    return render(request,'404.html')

# def BlogPostLike(request):
#     post = get_object_or_404(Post, id=request.POST.get('slug'))
#     post.likes.add(request.user)

#     return JsonResponse({"msg":"success"})


# def BlogPostUnlike(request):
#     post = get_object_or_404(Post, id=request.POST.get('slug'))
#     post.likes.remove(request.user)
    
#     return JsonResponse({"msg":"success"})



