from django.urls import path

from . import views

urlpatterns=[
 
    path('',views.yvideo,name='yvideo'),
    path('video/<int:id>', views.play_this_youtube,name='play_yvideo')
    
    
]