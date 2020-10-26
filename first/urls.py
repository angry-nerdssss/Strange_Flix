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
    path('all_svideos/<str:type>/', views.all_svideos, name='all_svideos'),
    path('mycorner', views.mycorner, name='mycorner'),
    path('mycorner/liked_videos_page',
         views.liked_videos_page, name='liked_videos_page'),
    path('search',views.search,name='search'),
    path('search_tag/<slug:slug>/', views.search_tag, name='search_tag'),
    path('search_tagbyname', views.search_tagbyname, name='search_tagbyname'),
    #path('search_tag2/<slug:slug>/', views.search_tag2, name='search_tag2'),
]
