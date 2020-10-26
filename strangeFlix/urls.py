
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django_email_verification import urls as mail_urls
from django.conf.urls.static import static


urlpatterns = [
    path('youtube_video/', include('youtube_video.urls')),#urls of youtube_video app
    path('',include('first.urls')),#urls of first app
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),#for allauth package
    path('email/', include(mail_urls)),#for sending emails
    path('oauth/', include('social_django.urls', namespace='social')),#for social logins
    path('storage_video/',include('storage_video.urls')),#urls of storage_video app
    path('comment/', include('comment.urls')),#urls of commenting functionalities
    
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
