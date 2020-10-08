from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from taggit.models import Tag
from .models import Video
from .forms import VideoForm

def svideo_upload_view(request):
    videos=Video.objects.order_by('-publish_date')
    common_tags = Video.tags.most_common()[:4]
    form= VideoForm(request.POST,request.FILES)
    if form.is_valid():
        newvideo = form.save(commit=False)
        newvideo.slug = slugify(newvideo.title)
        newvideo.save()
        form.save_m2m()
    context= {'videos': videos,
              'common_tags':common_tags,
              'form': form,
              }
    return render(request, 'svideo_upload.html', context)




def svideo_detail_view(request,slug):
    video = get_object_or_404(Video, slug=slug)
    context = {
        'video':video,
    }
    return render(request, 'svideo_detail.html', context)


def svideo_tagged(request,slug):
    tag = get_object_or_404(Tag,slug=slug)
    common_tags = Video.tags.most_common()[:4]
    videos = Video.objects.filter(tags=tag)
    context={
        'tag':tag,
        'common_tags':common_tags,
        'videos':videos,
        
    }
    return render(request,'svideo_upload.html',context)

def video(request,id):
    video =get_object_or_404(Video,pk=id)
    context={
        'video':video,
    }
    return render(request,'video.html',context)