from django.urls import path,include
from . import views
urlpatterns = [
    path('create/',views.CreateView,name='create'),
    path('comment/',views.CommentView,name='comment'),
    path('delete-comment/',views.DeleteCommentView,name='deleteComment'),
    path('drafts/',views.draftBlogView,name='drafts'),
    path('subscribe/',views.subscribeView,name='subscribe'),
    path('<str:user>/',views.subsite,name='site'),
    path('<str:user>/<str:slug>/',views.subsiteBlog,name='blog'),
    path('<str:user>/<str:slug>/update/',views.UpdateView,name='update'),
    path('<str:user>/<str:slug>/delete/',views.DeleteView,name='delete'),
    # path('blog_like/',views.BlogPostLike,name="blog_like"),
    # path('blog_unlike/',views.BlogPostUnlike,name="blog_unlike")
]
