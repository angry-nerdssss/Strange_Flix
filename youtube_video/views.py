from django.shortcuts import render, get_object_or_404
from .models import Item
# Create your views here.

def yvideo(request):
    obj=Item.objects.all()
    return render(request,'index.html',{'obj':obj})

def play_this_youtube(request,id):
    item = get_object_or_404(Item,pk = id)
    #print(f"***********{item.video.Thumbnail}**************")
    return render(request,'youtube_video_player.html',{'new_url':item.video})
