from django.urls import path

from . import views

urlpatterns=[
    path('',views.index,name='index'),#this path is for main page
    path('register',views.register,name='register'),#to call the register page
    path('login',views.login,name='login'),#to call the login page
    path('logout',views.logout,name='logout'),#to call the logout function
    path('subscription', views.subscription, name='subscription'),#to call the subscription page to accept any subscription

]