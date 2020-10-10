from django.urls import path

from . import views

urlpatterns=[
 
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('subscription', views.subscription, name='subscription'),
    path('video_upload_choice', views.video_upload_choice, name='video_upload_choice'),
    path('about_us', views.about, name = 'about_us')

]