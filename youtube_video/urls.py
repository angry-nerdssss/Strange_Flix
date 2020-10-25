from django.urls import path

from . import views

urlpatterns = [
     # this path is to call function to the player
     path('video/<int:id>/', views.play_this_youtube, name='play_yvideo'),
     # this path is to go for the tags
     path('tag/<slug:slug>/', views.yvideo_tagged, name='tagged'),
     # this path is to go for the detailview page of the selected video
     path('detail/<slug:slug>/', views.yvideo_detail_view, name='detail'),
     # this path is call function to upload videos from the admin
     path('add_video/', views.yvideo_upload_view, name='add_youtube_video'),
     path('favourite_yvideo/',
         views.favourite_yvideo, name='favourite_yvideo'),
     path('yvideo_like/', views.yvideo_like, name='yvideo_like'),
     path('yvideo_dislike/', views.yvideo_dislike, name='yvideo_dislike'),
     path('deleteyvideo/<int:id>/', views.delete_yvideo, name='delete_yvideo'),



]
