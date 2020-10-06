from django.shortcuts import render, get_object_or_404
from .models import Item
from django.template.defaultfilters import slugify
from .forms import ItemForm
from taggit.models import Tag

def yvideo(request):
    items=Item.objects.all()
    context={
        'items':items,
    }
    return render(request,'index.html',context)

def play_this_youtube(request,id):
    item = get_object_or_404(Item,pk = id)
    context={
        'item':item,
    }
    #print(f"****{item.video.Thumbnail}*****")
    return render(request,'youtube_video_player.html',context)

def yvideo_upload_view(request):
    items = Item.objects.order_by('-publish_date')
    common_tags = Item.tags.most_common()[:4]
    form = ItemForm(request.POST)
    if form.is_valid():
        newitem = form.save(commit=False)
        newitem.slug = slugify(newitem.title)
        newitem.save()
        form.save_m2m()
    context={
        'items':items,
        'common_tags':common_tags,
        'form':form,

    }
    return render(request,'yvideo_upload.html',context)

def yvideo_detail_view(request,slug):
    item = get_object_or_404(Item, slug=slug)
    context = {
        'item':item,
    }
    return render(request, 'yvideo_detail.html', context)


def yvideo_tagged(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    common_tags = Item.tags.most_common()[:4]
    items = Item.objects.filter(tags=tag)
    context={
        'tag':tag,
         'common_tags':common_tags,
        'items':items,
        
    }
    return render(request,'yvideo_upload.html',context)