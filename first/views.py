from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django_email_verification import sendConfirm
from storage_video.models import Video
from youtube_video.models import Item
from .models import Feedback

#this function is to render to the main page when the user first searches for the site
def index(request) :
    items = Item.objects.all()
    videos = Video.objects.all()
    showRegister=False
    showLogin=False
    context = {
        'showRegister':showRegister,
        'showLogin':showLogin,
        'items':items,
        'videos':videos,
    }
    return render(request,"index.html",context)

#this function is to set login conditions and functionality
def login(request) :
     if request.method == 'POST' :
         username = request.POST['email']
         password = request.POST['password']
          # by writing this we are checking whether the entered username and password are of the same user or not 
         user = auth.authenticate(username=username,password=password)
         if user is not None :
             auth.login(request,user)
             return redirect('/')
         else :
             messages.info(request,'invalid credentials')
             return redirect('index.html',)
            
     else :
         return render(request,"login.html")


#this function is used to get user logged out
def logout(request) :
    auth.logout(request)
    request.session['member_id'] = 0
    return redirect('/')

##this function is to set register conditions and functionality
def register(request):
    if request.method == 'POST' :
        username=request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # by writing this condition we are checking that if password1 and password2 are equal or not 
        if password1==password2 :
            # by writing this condition we are checking that if this email is already registered or not
            if User.objects.filter(email=email).exists() :
               messages.info(request,'email taken already')
               context={
                    'showRegister':True,
                    'showLogin':False,
                    'messages':messages,
               }
               return render('index.html',context)
            else :
                #user =User.objects.create_user(email=email,password=password1)
                # by writing this only we are hitting the database to store the information
                #user.save()
                user = get_user_model().objects.create(username=username,password=password1,email=email)
                sendConfirm(user)
                
                print('user created')
                return redirect('index') 
        else :
            messages.info(request,'password not matching')
            return redirect('register')
        return('/')  
    else :
        return render(request,'reg.html')


#this function will simply reder you to subscription page
def subscription(request):
    return render(request,"subscription.html")

def feedback(request):
    feedbacks=Feedback.objects.all()
    context={
        'feedbacks':feedbacks,
    }
    return render(request,'feedback.html',context)

##this function is to take feedback
def feedback(request) :
    name = request.POST['name']
    email = request.POST['email']
    subject = request.POST['subject']
    message = request.POST['message']
    feed = Feedback(name=name,email=email,subject=subject,message=message)
    # by writing this only we are hitting the database to store the information
    feed.save()
    
    return redirect('index')

