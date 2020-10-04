from django.shortcuts import render

# Create your views here.

from .models import Item


def yvideo(request):
    obj=Item.objects.all()
    return render(request,'index.html',{'obj':obj})

def play_this_youtube(request,url):
    new_url=url
    return render(request,'youtube_video_player.html',{'new_url':new_url})
