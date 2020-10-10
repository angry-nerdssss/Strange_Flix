
from django.db import models
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
#this model is to save all the details of the uploaded video from the admin
class Video(models.Model):
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")
    poster= models.FileField(upload_to='images/', null=True, verbose_name="")
    title=models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    publish_date= models.DateField(auto_now_add=True)
    description=models.TextField(max_length=500)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    comments = GenericRelation(Comment)
    def __str__(self):
        return self.title + ": " + str(self.videofile)
