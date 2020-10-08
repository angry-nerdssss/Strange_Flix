from django.contrib import admin
from embed_video.admin import AdminVideoMixin
from .models import Video


admin.site.register(Video)