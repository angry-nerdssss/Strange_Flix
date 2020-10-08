from django.urls import path

from . import views

urlpatterns=[
 
    #path('',views.yvideo,name='yvideo'),
    path('video/<int:id>/', views.play_this_youtube,name='play_yvideo'),
    path('tag/<slug:slug>/',views.yvideo_tagged,name='tagged'),
    path('detail/<slug:slug>/',views.yvideo_detail_view,name='detail'),
    path('add_video/',views.yvideo_upload_view,name='add_youtube_video'),
]