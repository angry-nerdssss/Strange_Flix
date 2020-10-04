from django.shortcuts import render, get_object_or_404
from .models import Item



def yvideo(request):
    obj=Item.objects.all()
    return render(request,'index.html',{'obj':obj})

def play_this_youtube(request,id):
    item = get_object_or_404(Item,pk = id)
    return render(request,'youtube_video_player.html',{'new_url':item.video})
