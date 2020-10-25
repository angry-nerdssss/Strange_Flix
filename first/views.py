from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
from storage_video.models import Video
from youtube_video.models import Item
from .models import Feedback, Subscription

# this function is to render to the main page when the user first searches for the site


def index(request):
    items = Item.objects.all()
    videos = Video.objects.all()
    showRegister = False
    showLogin = False

    recommended_videos1 = Video.objects.order_by('-publish_date')[:12]
    # recommended_videos=recommended_videos.order_by('-publish_date')

    recommended_videos2 = sorted(recommended_videos1, key=lambda o: o.views)
    recommended_videos = reversed(recommended_videos2)

    paid = False
    try:
        current_user = User.objects.get(username=request.user.username)
    except:
        context = {
            'showRegister': showRegister,
            'showLogin': showLogin,
            'items': items,
            'videos': videos,

            'recommended_videos': recommended_videos,
            'paid': paid,
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

        'recommended_videos': recommended_videos,
        'paid': paid,
    }
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
    return render(request, "subscription.html")


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

    return redirect('show_feedback')

# this function is to take user to about.html page


def about(request):
    return render(request, "about.html")


def subscribed_user(request):
    try:
        Subscription.objects.get(user=request.user)

    except:
        return redirect('index')

    subscription = Subscription.objects.get(user=request.user)
    subscription.paid = True
    subscription.save()
    return redirect('index')

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
