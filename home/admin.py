from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Blog)
admin.site.register(models.Comment)
admin.site.register(models.Subscriber)
admin.site.register(models.UserProfile)
admin.site.register(models.Report)