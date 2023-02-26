from django import template
from home.models import *
register =template.Library()

@register.filter(name='get')
def get(dict,key):
    return dict.get(key)

@register.filter(name='similar')
def similar(user):
    posts  = Blog.objects.filter(user=user).order_by('created_at')[0 : 3]
    return posts

@register.filter(name='getprofile')
def getprofile(user):
    profile = UserProfile.objects.filter(user=user).first()
    return profile.profilePic

@register.filter(name='getcommentsCount')
def getcommentsCount(blog):
    comments = Comment.objects.filter(post=blog).count()
    return comments