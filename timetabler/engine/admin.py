from django.contrib import admin
from django.apps import apps
from .models import UserData, Task, PixelArt, Tag, Achievement

# Add models to Django's admin interface for easy manipulation
admin.site.register(Task)
admin.site.register(UserData)
admin.site.register(Tag)
admin.site.register(PixelArt)
admin.site.register(Achievement)