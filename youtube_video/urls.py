from django.urls import path

from . import views

urlpatterns=[
 
    path('yvideo',views.yvideo,name='yvideo'),
    
]