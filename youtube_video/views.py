from django.shortcuts import render

# Create your views here.

from .models import Item

def yvideo(request) :
    obj = Item.objects.all()

from .models import Item
# Create your views here.

def yvideo(request):
    obj=Item.objects.all()
    return render(request,'index.html',{'obj':obj})