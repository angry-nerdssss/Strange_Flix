from django import forms
from .models import Video


#this form is to take input of video details from the admin
class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields = [
            'videofile',
            'poster',
            'title',
            'category',
            'tags',
            'description',
        ]