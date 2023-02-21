from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
import os
# Create your models here.
choice = [
    ('1', 'Draft'),
    ('2', 'Published'),
]
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profilePic= models.ImageField(upload_to='profile/',default='profile/default1.png')
    about = models.CharField(max_length=255,blank=True)
    siteTitle= models.CharField(max_length=255,blank=True)
    siteDescription = models.TextField(blank=True)
    siteImage= models.ImageField(upload_to='site/',default='site/default.png')

    def __str__(self):
        return self.user.username
    
    def delete(self,*args,**kwargs):
        if os.path.isfile(self.profilePic.path) and self.profilePic.name is not 'profile/default1.png':
            os.remove(self.profilePic.path)
        
        if os.path.isfile(self.siteImage.path) and self.siteImage.name is not 'site/default.png':
            os.remove(self.siteImage.path)

        super(UserProfile, self).delete(*args,**kwargs)


class Blog(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    slug = models.CharField(null=False,blank=False,max_length=255)
    title = models.CharField(max_length=150,blank=False,null=False)
    description = models.CharField(max_length=250,blank=True)
    tags = TaggableManager()
    image = models.ImageField(upload_to='blog/',default='blog/default.png')
    body = HTMLField()
    status= models.CharField(choices=choice,default='1',max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    class Meta:
        unique_together = ('user', 'slug',)
    
    def delete(self,*args,**kwargs):
        if os.path.isfile(self.image.path) and self.image.name is not 'blog/default.png':
            os.remove(self.image.path)
        super(Blog, self).delete(*args,**kwargs)



class Subscriber(models.Model):
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    email=models.EmailField(max_length=255)

    def __str__(self):
        return self.email + " | " + self.user.user.username

class Report(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    report = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    commentBody = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return "comment by "+self.user.user.username