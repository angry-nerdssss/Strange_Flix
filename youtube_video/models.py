from django.db import models
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
from datetime import date
class Item(models.Model):
    video = models.URLField(max_length = 200)  
    title=models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    publish_date= models.DateField(auto_now_add=True)
    description=models.TextField(max_length=500)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    def __str__(self):
        return self.video