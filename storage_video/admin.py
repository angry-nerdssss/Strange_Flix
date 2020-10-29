from django.contrib import admin
from embed_video.admin import AdminVideoMixin

from .models import Video
from .models import Time


admin.site.register(Video)
admin.site.register(Time)

