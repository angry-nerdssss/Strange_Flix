from django import forms
from .models import Item

#this form is to take input of the youtube video linkes and the video details
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'video',
            'title',
            'category',
            'genre',
            'tags',
            'description',
        ]