from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),  # this path is for main page
    # to call the register page
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),  # to call the login page
    path('logout', views.logout, name='logout'),  # to call the logout function
    # to call the subscription page to accept any subscription
    path('subscription', views.subscription, name='subscription'),
    path('about_us', views.about, name='about_us'),
    path('feedback', views.get_feedback, name='feedback'),
    path('showfeedback', views.show_feedback, name='show_feedback'),
    path('subscribed_user', views.subscribed_user, name='subscribed_user'),
    path('ajax/validate_username/$',
         views.validate_username, name='validate_username'),
    path('notification_panel', views.notification_panel, name='notification_panel'),
]
