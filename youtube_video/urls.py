from django.urls import path

from . import views
from .views import UpdateItemVote
urlpatterns=[
    path('video/<int:id>/', views.play_this_youtube,name='play_yvideo'),#this path is to call function to the player
    path('tag/<slug:slug>/',views.yvideo_tagged,name='tagged'),#this path is to go for the tags
    path('detail/<slug:slug>/',views.yvideo_detail_view,name='detail'),#this path is to go for the detailview page of the selected video
    path('add_video/',views.yvideo_upload_view,name='add_youtube_video'),#this path is call function to upload videos from the admin
    path('requirement/<int:item_id>/<str:opition>', views.UpdateItemVote.as_view(), name='requirement_item_vote'),
]