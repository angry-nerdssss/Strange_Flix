from django.urls import path

from . import views
from .views import UpdateVideoVote
urlpatterns=[
    path('svideo/<int:id>/',views.video,name='play_svideo'),
    path('stag/<slug:slug>/',views.svideo_tagged,name='s_tagged'),
    path('sdetail/<slug:slug>/',views.svideo_detail_view,name='s_detail'),
    path('sadd_video/',views.svideo_upload_view,name='add_storage_video'),
    path('requirement/<int:video_id>/<str:opition>', views.UpdateVideoVote.as_view(), name='requirement_video_vote'),
]