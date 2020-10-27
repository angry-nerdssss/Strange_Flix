from django.shortcuts import render, redirect, get_object_or_404,reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
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
# this function is to render to the main page when the user first searches for the site


def index(request):

    # genre
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
    showRegister = False
    showLogin = False
    count = 0

    recommended_videos1 = Video.objects.order_by('-publish_date')[:6]
    # recommended_videos=recommended_videos.order_by('-publish_date')

    recommended_videos2 = sorted(recommended_videos1, key=lambda o: o.views)
    recommended_videos = reversed(recommended_videos2)
    recommended_items1 = Item.objects.order_by('-publish_date')[:6]
    recommended_items2 = sorted(recommended_items1, key=lambda o: o.views)
    recommended_items = reversed(recommended_items2)

    paid = False
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
        }
        return render(request, "index.html", context)

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
                print('user created')
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


# this function will simply reder you to subscription page
def subscription(request):
    try:
        Subscription.objects.get(user=request.user)

    except:
        return redirect('index')
    
    subscription = Subscription.objects.get(user=request.user)
    paid = subscription.paid
    delta = datetime.now().date()
    b=datetime.now().date()
    days = delta-b
    print(days)
    if paid == 'True' :
        if subscription.deadline >= delta :
            days =  subscription.deadline-delta
            print(days.days)
        else :
            subscription.paid=False
            paid=False
            subscription.save()
    context={
        'paid':paid,
        'days':days.days
    }
    return render(request, "subscription.html",context)

def subscribed_user(request):
    print("workon subscribed_user0")
    try:
        Subscription.objects.get(user=request.user)

    except:
        return redirect('index')

    subscription = Subscription.objects.get(user=request.user)
    if subscription.paid == 'True':
        
        subscription.deadline=subscription.deadline + timedelta(days=30)
        
    else:
        subscription.deadline=datetime.now().date() + timedelta(days=30)
        subscription.paid = True
    print("workon subscribed_user1")
    subscription.save()
    return render(request, "about.html")



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
    #return HttpResponseRedirect(reverse(request.path_info))

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


def validate_username(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    email_valid = validateEmail(email)
    print(email_valid)

    data = {
        'is_username_taken': User.objects.filter(username__iexact=username).exists(),
        'is_email_taken': User.objects.filter(email=email).exists() or not email_valid
    }
    print(data)
    if data['is_username_taken']:
        data['username_error_message'] = 'A user with this username already exists.'
    if data['is_email_taken']:
        data['email_error_message'] = 'Email already registered.'
        if not email_valid:
            data['email_error_message'] = 'Email invalid'

    return JsonResponse(data)


def notification_panel(request):
    videos = Video.objects.all()
    context = {
        'videos': videos,

    }
    return render(request, "notification_panel.html", context)


def all_svideos(request, type):
    videos = Video.objects.filter(genre=type)
    items = Item.objects.filter(genre=type)
    context = {
        'videos': videos,
        'items': items,
    }
    return render(request, "all_svideos.html", context)


def all_yvideos(request, type):
    videos = Item.objects.filter(genre=type)
    context = {
        'videos': videos,
    }
    return render(request, "all_svideos.html", context)


def mycorner(request):
    videos=Video.objects.all()
    items=Item.objects.all()
    show=True
    context={
        'videos':videos,
        'items':items,
        'show':show
    }
    return render(request, 'mycorner.html',context)


def liked_videos_page(request):
    context = {
        'heading': "Liked Videos",
    }
    return render(request, 'allVideos.html', context)


strings = []
def subString(Str,n):
    
    for l in range(1,n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            util_string=""
            for k in range(i,j + 1):
                util_string=util_string+Str[k]
                
            x=len(Str)
            x=x//2
            if len(util_string)>x :
                strings.append(util_string)
                print(util_string)
            

def search(request):
    if request.method=='POST':
        video_name=request.POST['video_name']

        #main_video=Video.objects.get(title__iexact=video_name) 
        #related_video=Video.objects.filter(title__istartswith=video_name)
        subString(video_name,len(video_name))
        queryset = Video.objects.none()

        for string in strings :
            queryset |=Video.objects.filter(title__icontains=string)
        recommended_video = reversed(queryset)

        queryset = Item.objects.none()
        for string in strings :
            queryset |=Item.objects.filter(title__icontains=string)
        queryset.distinct()
        recommended_item = reversed(queryset)
        """
        for obj in recommended_video:
            print(obj.title)

        print(" and ")
        for obj in recommended_item:
            print(obj.title)
        """
        ctx={
            'videos':recommended_video,
            'items':recommended_item
        }
        
        return render(request,'all_svideos.html',ctx)
        """
        main_item=Item.objects.get(title__iexact=video_name) 
        recommends_item=Item.objects.filter(title__istartswith=video_name)
        """

def search_tag(request,slug):
    tag = get_object_or_404(Tag, slug=slug)
    print(tag.name)
    videos=Video.objects.filter(tags=tag)
    items=Item.objects.filter(tags=tag)
    context={
        'tag':tag,
        'videos':videos,
        'items':items,
    }
    return render(request,'all_svideos.html',context)

def search_tagbyname(request):
    tag=request.POST['tag_name']
    all_videos=Video.objects.all()
    queryset=Video.objects.none()
    for video in all_videos:
        if video.tags.filter(name=tag).exists():
            queryset |=Video.objects.filter(id=video.id)
    videos=queryset

    all_items=Item.objects.all()
    queryset=Item.objects.none()
    for item in all_items:
        if item.tags.filter(name=tag).exists():
            queryset |=Item.objects.filter(id=item.id)
    items=queryset
    context={
        'tag':tag,
        'videos':videos,
        'items':items,
    }
    return render(request,'all_svideos.html',context)
