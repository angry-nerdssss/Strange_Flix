from django.contrib import admin
from .models import Feedback, Subscription, Theme
# Register your models here.
admin.site.register(Feedback)
admin.site.register(Theme)
admin.site.register(Subscription)
