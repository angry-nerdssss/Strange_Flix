from django.shortcuts import render, get_object_or_404
from .models import Item,Like,Dislike
from django.template.defaultfilters import slugify
from .forms import ItemForm
from taggit.models import Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

#this function is to play the selected video
def play_this_youtube(request,id):
    item = get_object_or_404(Item,pk = id)
    context={
        'item':item,
    }
    return render(request,'youtube_video_player.html',context)

#this function is to upload the svideo_upload.html file when the user fills the form to upload video
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

#this function is to redirect the admin to the page to the page where he can see details of the selected video from the list
def yvideo_detail_view(request,slug):
    item = get_object_or_404(Item, slug=slug)
    context = {
        'item':item,
    }
    return render(request, 'yvideo_detail.html', context)

#this function is to show videos as per the selected common tags 
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

        


class UpdateItemVote(LoginRequiredMixin, View):
    
    def get(self, request, *args, **kwargs):

        item_id = self.kwargs.get('item_id', None)
        opition = self.kwargs.get('opition', None) # like or dislike button clicked

        item = get_object_or_404(Item, id=item_id)

        try:
            # If child DisLike model doesnot exit then create
            item.dis_likes
        except Item.dis_likes.RelatedObjectDoesNotExist as identifier:
            Dislike.objects.create(item = item)

        try:
            # If child Like model doesnot exit then create
            item.likes
        except Item.likes.RelatedObjectDoesNotExist as identifier:
            Like.objects.create(item = item)

        if opition.lower() == 'like':

            if request.user in item.likes.users.all():
                item.likes.users.remove(request.user)
            else:    
                item.likes.users.add(request.user)
                item.dis_likes.users.remove(request.user)

        elif opition.lower() == 'dis_like':

            if request.user in item.dis_likes.users.all():
                item.dis_likes.users.remove(request.user)
            else:    
                item.dis_likes.users.add(request.user)
                item.likes.users.remove(request.user)
        else:
            return HttpResponseRedirect(reverse('play_yvideo', args=[str(item.id)]))
        return HttpResponseRedirect(reverse('play_yvideo', args=[str(item.id)]))