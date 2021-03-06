from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
from .models import Video, Time
from first.models import Subscription
from .forms import VideoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.views.generic import View
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
# this function is to upload the svideo_upload.html file when the user fills the form to upload video


def svideo_upload_view(request):
    # we are showing all the uploaded videos according to their publish dates
    videos = Video.objects.order_by('-publish_date')
    # we are also creating the common tags to see only videos accordingly
    common_tags = Video.tags.most_common()[:4]
    form = VideoForm(request.POST, request.FILES)
    if form.is_valid():
        newvideo = form.save(commit=False)
        newvideo.slug = slugify(newvideo.title)
        newvideo.save()
        #we are using save_m2m() instead of save() as we have to take input of multiple tags at a time
        form.save_m2m()
    context = {'videos': videos,
               'common_tags': common_tags,
               'form': form,
               }
    return render(request, 'svideo_upload.html', context)


# this function is to redirect the admin to the page to the page where he can see details of the selected video from the list
def svideo_detail_view(request, slug):
    video = get_object_or_404(Video, slug=slug)
    context = {
        'video': video,
    }
    return render(request, 'svideo_detail.html', context)

# this function is to show videos as per the selected common tags
def svideo_tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Video.tags.most_common()[:4]
    #we are filtering the videos through tags
    videos = Video.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'common_tags': common_tags,
        'videos': videos,

    }
    return render(request, 'svideo_upload.html', context)




# this function is to play the selected video
def video(request, id):
    #handling the exception user is authenticated or not
    try:
        current_user = User.objects.get(username=request.user.username)
    except:
        return redirect('index')
    current_user = User.objects.get(username=request.user.username)
    if(current_user.is_superuser):
        current_time = 0.0
        video = get_object_or_404(Video, pk=id)
        if Time.objects.filter(username=current_user.username).filter(video_title=video.title).exists():
            obj = Time.objects.filter(username=current_user.username).filter(
                video_title=video.title)[:1].get()
            current_time = obj.currentTime

        context = {
            'video': video,
            'current_time': current_time,
        }
        return render(request, 'video.html', context)
    try:
        Subscription.objects.get(user=request.user)
    except:
        Subscription.objects.create(user=request.user)
    subscription=Subscription.objects.get(user=request.user)
    if subscription.paid == 'False':
        return redirect('subscription')

    video = get_object_or_404(Video, pk=id)
    # allVideos = Video.objects.all()
    # count_videos = allVideos.count()
    # # oldvideo = get_object_or_404(Video, pk=id)
    # # newid = oldvideo.id + 1
    # nextid = Video.objects.order_by('-id').first().id + 1
    # nextvideo = Video.objects.get(id=nextid)
    # video2 = get_object_or_404(Video, pk=id)
    # print(video2)
    current_time = 0.0
    if Time.objects.filter(username=current_user.username).filter(video_title=video.title).exists():
        obj = Time.objects.filter(username=current_user.username).filter(
            video_title=video.title)[:1].get()
        current_time = obj.currentTime

    context = {
        'video': video,
        'current_time': current_time,
        # 'nvideo': allVideos,
    }
    return render(request, 'video.html', context)





# this function is to implement autoplay
def next_video(request, id):
    allVideos = Video.objects.all()
    last_video = Video.objects.last()
    count_videos = last_video.id
    nextid = (id + 1) % (count_videos+1)
    # if nextid == 0:
    #     nextid = 1
    if not Video.objects.filter(id=nextid).exists():
        nextid = (nextid + 1) % (count_videos+1)
    # try:
    #     video = Video.objects.get(id=nextid)
    # except:
    #     return next_video(request, nextid)
    
    return video(request, nextid)  

#this is to implement like feature
@require_POST
def svideo_like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        video = get_object_or_404(Video, slug=slug)
        liked = True
        disliked = False
        if video.likes.filter(id=user.id).exists():
            # user has already liked this video
            # remove like/user
            video.likes.remove(user)
            message = 'You disliked this'
            liked = False
        else:
            # add a new like for a video
            video.likes.add(user)
            if video.dislikes.filter(id=user.id).exists():
                video.dislikes.remove(user)

            message = 'You liked this'

    ctx = {'likes_count': video.total_likes, 'message': message,
           'dislikes_count': video.total_dislikes, 'liked': liked, 'disliked': disliked}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
    return HttpResponseRedirect(reverse('play_svideo', args=[str(video.id)]))


#this is to implement dislike feature
@require_POST
def svideo_dislike(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        video = get_object_or_404(Video, slug=slug)
        liked = False
        disliked = True
        if video.dislikes.filter(id=user.id).exists():
            # user has already liked this video
            # remove like/user
            video.dislikes.remove(user)
            disliked = False
            message = 'You disliked this'
        else:
            # add a new like for a video
            video.dislikes.add(user)
            if video.likes.filter(id=user.id).exists():
                video.likes.remove(user)
            message = 'You liked this'

    ctx = {'dislikes_count': video.total_dislikes, 'message': message,
           'likes_count': video.total_likes, 'liked': liked, 'disliked': disliked}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
    return HttpResponseRedirect(reverse('play_svideo', args=[str(video.id)]))

#to add a storage video to your favourites
def favourite_svideo(request):
    title = request.GET.get('title', None)
    try:
        currentUser = User.objects.get(username=request.user.username)

    except:
        return redirect('login')
    currentUser = User.objects.get(username=request.user.username)
    added = True
    video = Video.objects.get(title=title)
    if video.favourite.filter(id=currentUser.id).exists():
        video.favourite.remove(request.user)
        added = False
    else:
        video.favourite.add(request.user)
    ctx = {'added': added, }
    return HttpResponse(json.dumps(ctx), content_type='application/json')

#to replay the video from where the user has left when he again visits that video
def getCurrentTime(request):
    current_time = request.GET.get('currentTime', None)
    title = request.GET.get('title', None)
    try:
        current_user = User.objects.get(username=request.user.username)
    except:
        return redirect('login')
    current_user = User.objects.get(username=request.user.username)
    if Time.objects.filter(username=current_user.username).filter(video_title=title).exists():
        time = Time.objects.filter(username=current_user.username).filter(
            video_title=title)[:1].get()
        time.currentTime = current_time
        time.save()
    else:
        time = Time.objects.create(
            username=current_user.username, video_title=title, currentTime=current_time)
    ctx = {}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

#to keep the record the no of views and to show it to the users also
def increase_views(request):
    title = request.GET.get('title', None)
    try:
        current_user = User.objects.get(username=request.user.username)
    except:
        return redirect('login')
    video = Video.objects.get(title=title)
    video.views = video.views+1
    video.save()
    ctx = {}
    return HttpResponse(json.dumps(ctx), content_type='application/json')


# delete view for details
def delete_svideo(request, id):
    # dictionary for initial data with
    # field names as keys
    # fetch the object related to passed id
    context = {}
    obj = get_object_or_404(Video, id=id)
    # delete object
    obj.delete()
    # after deleting redirect to
    # home page
    return HttpResponseRedirect("/")

#to flag a video
def flag_svideo(request):
    title = request.GET.get('title', None)
    try:
        currentUser = User.objects.get(username=request.user.username)

    except:
        return redirect('login')
    currentUser = User.objects.get(username=request.user.username)
    added = True
    video = Video.objects.get(title=title)
    if video.flag.filter(id=currentUser.id).exists():
        video.flag.remove(request.user)
        added = False
    else:
        video.flag.add(request.user)
    ctx = {'added': added, }
    return HttpResponse(json.dumps(ctx), content_type='application/json')
