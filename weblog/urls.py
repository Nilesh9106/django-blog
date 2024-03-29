from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('auth/', include("authentication.urls")),
    path('blog/', include("blog.urls")),
    path('dashboard/', include("dashboard.urls")),
    path('tag/', include("tag.urls")),
    path('verification/', include('verify_email.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
