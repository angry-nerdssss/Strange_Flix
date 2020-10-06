from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Item


admin.site.register(Item)