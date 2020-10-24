from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from taggit.models import Tag
from .models import Video
from first.models import Subscription
from .forms import VideoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
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
    try:
        current_user=User.objects.get(username=request.user.username)
    except:
        return redirect('index')
    
    subscription=Subscription.objects.get(user=request.user)
    if subscription.paid == 'False':
        return redirect('subscription')
    
    video =get_object_or_404(Video,pk=id)
    context={
        'video':video,
    }
    return render(request,'video.html',context)

""" class UpdateVideoVote(LoginRequiredMixin, View):
    
    
    def get(self, request, *args, **kwargs):

        video_id = self.kwargs.get('video_id', None)
        opition = self.kwargs.get('opition', None) # like or dislike button clicked

        video = get_object_or_404(Video, id=video_id)

        try:
            # If child DisLike model doesnot exit then create
            video.dis_likes
        except Video.dis_likes.RelatedObjectDoesNotExist as identifier:
            Dislike.objects.create(video = video)

        try:
            # If child Like model doesnot exit then create
            video.likes
        except Video.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(video = video)

        if opition.lower() == 'like':

            if request.user in video.likes.users.all():
                video.likes.users.remove(request.user)
            else:    
                video.likes.users.add(request.user)
                video.dis_likes.users.remove(request.user)

        elif opition.lower() == 'dis_like':

            if request.user in video.dis_likes.users.all():
                video.dis_likes.users.remove(request.user)
            else:    
                video.dis_likes.users.add(request.user)
                video.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('play_svideo', args=[str(video.id)]))
        return HttpResponseRedirect(reverse('play_svideo', args=[str(video.id)])) """


@require_POST
def svideo_like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        video = get_object_or_404(Video, slug=slug)
        if video.likes.filter(id=user.id).exists():
            # user has already liked this video
            # remove like/user
            video.likes.remove(user)
            message = 'You disliked this'
        else:
            # add a new like for a video
            video.likes.add(user)
            message = 'You liked this'

    ctx = {'likes_count': video.total_likes, 'message': message}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')