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

def index(request) :
    items = Item.objects.all()
    videos = Video.objects.all()
    context = {
        'items':items,
        'videos':videos,
    }
    return render(request,"index.html",context)





def login(request) :
     if request.method == 'POST' :
         email = request.POST['email']
         password = request.POST['password']
          # by writing this we are checking whether the entered username and password are of the same user or not 
         user = auth.authenticate(email=email,password=password)
         if user is not None :
             request.session['member_id'] = user.id
             auth.login(request,user)
             return redirect('/')
         else :
             messages.info(request,'invalid credentials')
             return redirect('login')
            
     else :
         return render(request,"login.html")



def logout(request) :
    auth.logout(request)
    request.session['member_id'] = 0
    return redirect('/')



def register(request):
    if request.method == 'POST' :
        
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # by writing this condition we are checking that if password1 and password2 are equal or not 
        if password1==password2 :
            # by writing this condition we are checking that if this email is already registered or not
            if User.objects.filter(email=email).exists() :
               messages.info(request,'email taken already')
               return redirect('register')
            else :
                #user =User.objects.create_user(email=email,password=password1)
                # by writing this only we are hitting the database to store the information
                #user.save()
                user = get_user_model().objects.create(password=password1, email=email)
                sendConfirm(user)
                
                print('user created')
                return redirect('index') 
        else :
            messages.info(request,'password not matching')
            return redirect('register')
        return('/')  
    else :
        return render(request,'reg.html')



def subscription(request):
    return render(request,"subscription.html")

def video_upload_choice(request):
    return render(request,"video_upload_choice.html")

def video(request):
    return render(request,"video.html")

def about(request):
    return render(request,"about.html")

def feedback(request):
    return render(request,"feedback.html")