from django.shortcuts import render, get_object_or_404,redirect
from .models import Item
from django.template.defaultfilters import slugify
from .forms import ItemForm
from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.views.decorators.http import require_POST
# this function is to play the selected video


def play_this_youtube(request, id):
    item = get_object_or_404(Item, pk=id)
    context = {
        'item': item,
    }
    return render(request, 'youtube_video_player.html', context)

# this function is to upload the svideo_upload.html file when the user fills the form to upload video


def yvideo_upload_view(request):
    items = Item.objects.order_by('-publish_date')
    common_tags = Item.tags.most_common()[:4]
    form = ItemForm(request.POST)
    if form.is_valid():
        newitem = form.save(commit=False)
        newitem.slug = slugify(newitem.title)
        newitem.save()
        form.save_m2m()
    context = {
        'items': items,
        'common_tags': common_tags,
        'form': form,

    }
    return render(request, 'yvideo_upload.html', context)

# this function is to redirect the admin to the page to the page where he can see details of the selected video from the list


def yvideo_detail_view(request, slug):
    item = get_object_or_404(Item, slug=slug)
    context = {
        'item': item,
    }
    return render(request, 'yvideo_detail.html', context)

# this function is to show videos as per the selected common tags


def yvideo_tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Item.tags.most_common()[:4]
    items = Item.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'common_tags': common_tags,
        'items': items,

    }
    return render(request, 'yvideo_upload.html', context)




def favourite_yvideo(request):
    print("views 0")
    title = request.GET.get('title',None)
    print("views 1")
    print(title)
    try:
        currentUser = User.objects.get(username=request.user.username)
    except:
        print("y")
        return redirect('login')
    currentUser = User.objects.get(username=request.user.username)
    print("views 3")
    added=True
    item=Item.objects.get(title=title)
    print(item.title)
    print(" ")
    print(item.description)
    if item.favourite.filter(id=currentUser.id).exists():
        item.favourite.remove(request.user)
        added=False
    else:
        item.favourite.add(request.user)
    ctx={'added':added,}
    return HttpResponse(json.dumps(ctx), content_type='application/json')



@require_POST
def yvideo_like(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        item = get_object_or_404(Item, slug=slug)
        liked=True
        disliked=False
        if item.likes.filter(id=user.id).exists():
            # user has already liked this video
            # remove like/user
            item.likes.remove(user)
            message = 'You disliked this'
            liked=False
        else:
            # add a new like for a video
            item.likes.add(user)
            if item.dislikes.filter(id=user.id).exists():
                item.dislikes.remove(user)

            message = 'You liked this'

    ctx = {'likes_count': item.total_likes, 'message': message,'dislikes_count': item.total_dislikes,'liked':liked,'disliked':disliked}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
    return HttpResponseRedirect(reverse('play_yvideo', args=[str(item.id)]))


@require_POST
def yvideo_dislike(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        item = get_object_or_404(Item, slug=slug)
        liked=False
        disliked=True
        if item.dislikes.filter(id=user.id).exists():
            # user has already liked this video
            # remove like/user
            item.dislikes.remove(user)
            disliked=False
            message = 'You disliked this'
        else:
            # add a new like for a video
            item.dislikes.add(user)
            if item.likes.filter(id=user.id).exists():
                item.likes.remove(user)
            message = 'You liked this'

    ctx = {'dislikes_count': item.total_dislikes, 'message': message,'likes_count': item.total_likes,'liked':liked,'disliked':disliked}
    # use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')
    return HttpResponseRedirect(reverse('play_yvideo', args=[str(item.id)]))


# delete view for details

def delete_yvideo(request, id):


    # dictionary for initial data with
    
    # field names as keys​​

    # fetch the object related to passed id
    context = {}
    obj = get_object_or_404(Item, id=id)

    # delete object

    obj.delete()

    # after deleting redirect to

    # home page

    return HttpResponseRedirect("/")

