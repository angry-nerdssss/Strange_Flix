from django.urls import path

from . import views
#from .views import UpdateVideoVote
urlpatterns = [
    path('svideo/<int:id>/', views.video, name='play_svideo'),
    path('stag/<slug:slug>/', views.svideo_tagged, name='s_tagged'),
    
    path('sdetail/<slug:slug>/', views.svideo_detail_view, name='s_detail'),
    path('sadd_video/', views.svideo_upload_view, name='add_storage_video'),
    #path('requirement/<int:video_id>/<str:opition>', views.UpdateVideoVote.as_view(), name='requirement_video_vote'),
    path('svideo_like/', views.svideo_like, name='svideo_like'),
    path('svideo_dislike/', views.svideo_dislike, name='svideo_dislike'),
    path('favourite_svideo/',
         views.favourite_svideo, name='favourite_svideo'),
    path('play/', views.getCurrentTime, name='getCurrentTime'),
    path('increase_views/', views.increase_views, name="increase_views"),
    path('deletesvideo/<int:id>/', views.delete_svideo, name='delete_svideo'),
    path('flag_svideo/',
         views.flag_svideo, name='flag_svideo'),
]
