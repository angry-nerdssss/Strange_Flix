from django.urls import path

from . import views

urlpatterns=[
 

    
    path('svideo/<int:id>/',views.video,name='play_svideo'),
    path('stag/<slug:slug>/',views.svideo_tagged,name='s_tagged'),
    path('sdetail/<slug:slug>/',views.svideo_detail_view,name='s_detail'),
    path('sadd_video/',views.svideo_upload_view,name='add_storage_video'),

]