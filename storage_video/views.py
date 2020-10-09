from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from taggit.models import Tag
from .models import Video
from .forms import VideoForm
 
#this function is to upload the svideo_upload.html file when the user fills the form to upload video
def svideo_upload_view(request):
    videos=Video.objects.order_by('-publish_date')#we are showing all the uploaded videos according to their publish dates
    common_tags = Video.tags.most_common()[:4]#we are also creating the common tags to see only videos accordingly
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



#this function is to redirect the admin to the page to the page where he can see details of the selected video from the list
def svideo_detail_view(request,slug):
    video = get_object_or_404(Video, slug=slug)
    context = {
        'video':video,
    }
    return render(request, 'svideo_detail.html', context)

#this function is to show videos as per the selected common tags 
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

#this function is to play the selected video
def video(request,id):
    video =get_object_or_404(Video,pk=id)
    context={
        'video':video,
    }
    return render(request,'video.html',context)