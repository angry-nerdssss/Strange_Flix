from django.shortcuts import render
from .models import Item
# Create your views here.

def yvideo(request):
    obj=Item.objects.all()
    return render(request,'index.html',{'obj':obj})