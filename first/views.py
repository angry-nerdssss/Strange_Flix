#importing all the required keywords and methods and models
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
from storage_video.models import Video
from youtube_video.models import Item
from .models import Feedback, Subscription
from taggit.models import Tag
from datetime import datetime, timedelta
import math

# this function is to render to the main page when the user first searches for the site
def index(request):
    # defining genre for movies
    FICTION = 'Fiction'
    MYSTERY = 'Mystery'
    THRILLER = 'Thriller'
    HORROR = 'Horror'
    HISTORICAL = 'Historical'
    ROMANCE = 'Romance'
    WESTERN = 'Western'
    FANTASY = 'Fantasy'
    ACTION = 'Action'
    COMEDY = 'Comedy'
    CRIME = 'Crime'
    ADVENTURE = 'Adventure'
    ANIMATION = 'Animation'
    WAR = 'War'
    GENRE_CHOICES = [

        (FICTION, 'Fiction'),
        (MYSTERY, 'Mystery'),
        (THRILLER, 'Thriller'),
        (HORROR, 'Horror'),
        (HISTORICAL, 'Historical'),
        (ROMANCE, 'Romance'),
        (WESTERN, 'Western'),
        (FANTASY, 'Fantasy'),
        (ACTION, 'Action'),
        (COMEDY, 'Comedy'),
        (CRIME, 'Crime'),
        (ADVENTURE, 'Adventure'),
        (ANIMATION, 'Animation'),
        (WAR, 'War'),
    ]

    items = Item.objects.all()
    videos = Video.objects.all()
    count = items.count()
    r_items = reversed(items)#reversing the queryset

    
    showRegister = False
    showLogin = False

    recommended_videos1 = Video.objects.order_by('-publish_date')[:6]#slicing 6 videos
    # recommended_videos=recommended_videos.order_by('-publish_date')


    #here we are sending the recommended videos
    recommended_videos2 = sorted(recommended_videos1, key=lambda o: o.views)
    recommended_videos = reversed(recommended_videos2)
    recommended_items1 = Item.objects.order_by('-publish_date')[:6]
    recommended_items2 = sorted(recommended_items1, key=lambda o: o.views)
    recommended_items = reversed(recommended_items2)


    paid = False
    #if the user is not logged in
    try:
        current_user = User.objects.get(username=request.user.username)
    except:
        context = {
            'showRegister': showRegister,
            'showLogin': showLogin,
            'items': items,
            'videos': videos,
            'genres': GENRE_CHOICES,

            'recommended_videos': recommended_videos,
            'recommended_items': recommended_items,
            'paid': paid,
            'count': count,
            'r_items': r_items,
        }
        return render(request, "index.html", context)


    #if the user is logged in
    if Subscription.objects.filter(user=request.user).exists():
        subscription = Subscription.objects.get(user=request.user)
        paid = subscription.paid
    context = {
        'showRegister': showRegister,
        'showLogin': showLogin,
        'items': items,
        'videos': videos,
        'genres': GENRE_CHOICES,
        'recommended_items': recommended_items,
        'recommended_videos': recommended_videos,
        'paid': paid,
        'count': count,
        'r_items': r_items,

    }
    """
    for i in range(12) :
        videos[i]=
    """
    return render(request, "index.html", context)



# this function is to set login conditions and functionality
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # by writing this we are checking whether the entered username and password are of the same user or not
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            context = {
                'showRegister': False,
                'showLogin': True,
            }
            return render(request, 'index.html', context)

    else:
        context = {
            'showRegister': False,
            'showLogin': True,
        }
        return render(request, 'index.html', context)


# this function is used to get user logged out
def logout(request):
    auth.logout(request)
    return redirect('/')


# this function is to set register conditions and functionality
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # by writing this condition we are checking that if password1 and password2 are equal or not
        if password1 == password2:
            # by writing this condition we are checking that if this email is already registered or not
            if User.objects.filter(email=email).exists():
                messages.info(request, 'email taken already')
                context = {
                    'showRegister': True,
                    'showLogin': False,

                }
                return render(request, 'index.html', context)
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username taken already')
                context = {
                    'showRegister': True,
                    'showLogin': False,
                }
                return render(request, 'index.html', context)
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                # by writing this only we are hitting the database to store the information
                user.save()
                subscription = Subscription.objects.create(user=user)
                subscription.save()
                sendConfirm(user)
                
                messages.info(request, 'Please check your e-mail')
                context = {
                    'showRegister': True,
                    'showLogin': False,
                }
            return render(request, 'index.html', context)
        else:
            messages.info(request, 'password not matching')
            context = {
                'showRegister': True,
                'showLogin': False,

            }
            return render(request, 'index.html', context)
        return('/')
    else:
        return render(request, 'reg.html')


# this function will simply reder you to subscription page after checking the user's subscription 
def subscription(request):
    try:
        Subscription.objects.get(user=request.user)
    except:
        
        return redirect('index')

    subscription = Subscription.objects.get(user=request.user)
    paid = subscription.paid
    delta = datetime.now().date()
    b = datetime.now().date()
    days = delta-b
    if paid == 'True':
        if subscription.deadline >= delta:
            days = subscription.deadline-delta
        else:
            subscription.paid = False
            paid = False
            subscription.save()
    context = {
        'paid': paid,
        'days': days.days
    }
    return render(request, "subscription.html", context)

#this function will update the payment status and subscription of the user
def subscribed_user(request):
    try:
        Subscription.objects.get(user=request.user)

    except:
        Subscription.objects.create(user=request.user)
        return redirect('index')

    subscription = Subscription.objects.get(user=request.user)
    if subscription.paid == 'True':

        subscription.deadline = subscription.deadline + timedelta(days=30)

    else:
        subscription.deadline = datetime.now().date() + timedelta(days=30)
        subscription.paid = True
    subscription.save()
    return redirect('/')

#this function is to show feedbacks from users to the admin
def show_feedback(request):
    feedbacks = Feedback.objects.order_by('-publish_date')
    context = {
        'feedbacks': feedbacks,
    }
    return render(request, 'feedback.html', context)

# this function is to take feedback
def get_feedback(request):
    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']
    feed = Feedback(name=name, email=email, subject=subject, message=message)
    # by writing this only we are hitting the database to store the information
    feed.save()
    return HttpResponseRedirect(reverse('index'))
    # return HttpResponseRedirect(reverse(request.path_info))

# this function is to take user to about.html page
def about(request):
    return render(request, "about.html")


# Email validation function
def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

#user validation function
def validate_username(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    email_valid = validateEmail(email)

    data = {
        'is_username_taken': User.objects.filter(username__iexact=username).exists(),
        'is_email_taken': User.objects.filter(email=email).exists() or not email_valid
    }
    if data['is_username_taken']:
        data['username_error_message'] = 'A user with this username already exists.'
    if data['is_email_taken']:
        data['email_error_message'] = 'Email already registered.'
        if not email_valid:
            data['email_error_message'] = 'Email invalid'

    return JsonResponse(data)

#this function is for the notification page for the admin
def notification_panel(request):
    videos = Video.objects.all()
    context = {
        'videos': videos,

    }
    return render(request, "notification_panel.html", context)

global_genre=[]
#this function will show the videos according to the selected genre
def all_svideos(request, types):
    global_genre.append(types)
    return genre_pagination(request,1)

def genre_pagination(request,page_no):
    videos = Video.objects.filter(genre=global_genre[-1])[(page_no-1)*2:page_no*2]
    items = Item.objects.filter(genre=global_genre[-1])[(page_no-1)*2:page_no*2]

    s_ranges1=Video.objects.filter(genre=global_genre[-1]).count()
    show1=True
    show2=True
    if videos.count() == 0 :
        show1=False
    
    s_ranges2=s_ranges1/2
    s_ranges3=math.ceil(s_ranges2)

    y_ranges1=Item.objects.filter(genre=global_genre[-1]).count()
    if items.count() == 0 :
        show2=False
    y_ranges2=y_ranges1/2
    y_ranges3=math.ceil(y_ranges2)
    
    
    if s_ranges3 > y_ranges3 :
        ranges3=s_ranges3
    else :
        ranges3=y_ranges3
    ranges=range(ranges3)
    types=global_genre[-1]
    context={
        'videos':videos,
        'items':items,
        'types':types,
        'page_no':page_no,
        'show1':show1,
        'show2':show2,
        'ranges':ranges,
    }
    return render(request,'all_svideos.html',context)
#this function is for the favourite and liked videos of the user
@login_required(login_url='login')
def mycorner(request):
    videos = Video.objects.all()
    items = Item.objects.all()
    show1 = False
    show2 = False
    show3 = False
    show4 = False
    for video in videos:
        if video.likes.filter(id=request.user.id).exists():
            show1 = True

    for item in items:
        if item.likes.filter(id=request.user.id).exists():
            show2 = True

    for video in videos:
        if video.favourite.filter(id=request.user.id).exists():
            show3 = True

    for item in items:
        if item.favourite.filter(id=request.user.id).exists():
            show4 = True
    context = {
        'videos': videos,
        'items': items,

        'show1': show1,
        'show2': show2,
        'show3': show3,
        'show4': show4,
    }
    return render(request, 'mycorner.html', context)

#this function is to just pass the liked videos to the page
def liked_videos_page(request):
    return svideo_pagination(request,1)

#this function is to make substrings of the the searched keyword for movies in the search bar
def subString(Str, n):
    strings = []
    for l in range(1, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            util_string = ""
            for k in range(i, j + 1):
                util_string = util_string+Str[k]

            x = len(Str)
            x = x//2
            if len(util_string) > x:
                strings.append(util_string)
    return strings

#this function will show the appropiate results according to the searches
def search(request):
    if request.method == 'POST':
        video_name = request.POST['video_name']

        # main_video=Video.objects.get(title__iexact=video_name)
        # related_video=Video.objects.filter(title__istartswith=video_name)
        strings = subString(video_name, len(video_name))
        queryset1 = Video.objects.none()
        for string in strings:
            
            queryset1 |= Video.objects.filter(title__icontains=string)
        recommended_video = reversed(queryset1)

        queryset2 = Item.objects.none()
        
        for string in strings:
            queryset2 |= Item.objects.filter(title__icontains=string)
        
        recommended_item = reversed(queryset2)
        ctx = {
            'videos': recommended_video,
            'items': recommended_item
        }
        strings = []
        return render(request, 'all_svideos_simple.html', ctx)
        """
        main_item=Item.objects.get(title__iexact=video_name) 
        recommends_item=Item.objects.filter(title__istartswith=video_name)
        """

#this function is to search acoording to the tags by clicking on them from any video
def search_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
   
    videos = Video.objects.filter(tags=tag)
    items = Item.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'videos': videos,
        'items': items,
    }
    return render(request, 'all_svideos_simple.html', context)

#this function is to search the according to the user given tags
def search_tagbyname(request):
    tag = request.POST['tag_name']
    all_videos = Video.objects.all()
    queryset = Video.objects.none()
    for video in all_videos:
        if video.tags.filter(name=tag).exists():
            queryset |= Video.objects.filter(id=video.id)
    videos = queryset

    all_items = Item.objects.all()
    queryset = Item.objects.none()
    for item in all_items:
        if item.tags.filter(name=tag).exists():
            queryset |= Item.objects.filter(id=item.id)
    items = queryset
    context = {
        'tag': tag,
        'videos': videos,
        'items': items,
    }
    return render(request, 'all_svideos_simple.html', context)


def allfav_videos(request):
    return svideo_fav_pagination(request,1)

def all_liked_yvideos(request):
    return yvideo_pagination(request,1)

def all_fav_yvideos(request):
    return yvideo_fav_pagination(request,1)

def svideo_pagination(request,page_no):
    videos=request.user.likes.all()[(page_no-1)*2:page_no*2]
    ranges1=request.user.likes.count()
    
    ranges2=ranges1/2
    ranges3=math.ceil(ranges2)
    ranges=range(ranges3)
    context={
        'videos':videos,
        'page_no':page_no,
        'ranges':ranges,
    }
    return render(request,'allVideos.html',context)

def svideo_fav_pagination(request,page_no):
    videos=request.user.fav_svideos.all()[(page_no-1)*2:page_no*2]
    ranges1=request.user.fav_svideos.count()
    
    ranges2=ranges1/2
    ranges3=math.ceil(ranges2)
    ranges=range(ranges3)
    context={
        'videos':videos,
        'page_no':page_no,
        'ranges':ranges,
    }
    return render(request,'allfav_videos.html',context)

def yvideo_pagination(request,page_no):
    videos=request.user.ylikes.all()[(page_no-1)*2:page_no*2]
    ranges1=request.user.ylikes.count()
    
    ranges2=ranges1/2
    ranges3=math.ceil(ranges2)
    ranges=range(ranges3)
    context={
        'videos':videos,
        'page_no':page_no,
        'ranges':ranges,
    }
    return render(request,'all_liked_yvideos.html',context)

def yvideo_fav_pagination(request,page_no):
    videos=request.user.fav_yvideos.all()[(page_no-1)*2:page_no*2]
    ranges1=request.user.fav_yvideos.count()
    
    ranges2=ranges1/2
    ranges3=math.ceil(ranges2)
    ranges=range(ranges3)
    context={
        'videos':videos,
        'page_no':page_no,
        'ranges':ranges,
    }
    return render(request,'all_fav_yvideos.html',context)
