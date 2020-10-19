
from django.db import models
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
#this model is to save all the details of the uploaded video from the admin

class Video(models.Model):
    #categories

    MOVIES='movie'

    TVSHOW='show'

    TVSERIES='series'



    #genre

    FICTION='Fiction'

    MYSTERY='Mystery'

    THRILLER= 'Thriller'

    HORROR='Horror'

    HISTORICAL='Historical'

    ROMANCE='Romance'

    WESTERN='Western'

    FANTASY='Fantasy'

    ACTION='Action'

    COMEDY='Comedy'

    CRIME='Crime'

    ADVENTURE='Adventure'

    ANIMATION='Animation'

    WAR='War'



    CATEGORY_CHOICES = [

        

        (MOVIES, 'Movies'),

        (TVSHOW, 'TV Show'),

        (TVSERIES, 'TV Series'),

    ]

    GENRE_CHOICES = [

        

        (FICTION, 'Fiction'),

        (MYSTERY, 'Mystery'),

        (THRILLER, 'Thriller'),

        (HORROR,'Horror'),

        (HISTORICAL,'Historical'),

        (ROMANCE,'Romance'),

        (WESTERN,'Western'),

        (FANTASY,'Fantasy'),

        (ACTION,'Action'),

        (COMEDY,'Comedy'),

        (CRIME,'Crime'),

        (ADVENTURE,'Adventure'),

        (ANIMATION,'Animation'),

        (WAR,'War'),

    ]

    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")
    poster= models.FileField(upload_to='images/', null=True, verbose_name="")
    title=models.CharField(max_length=100)
    category = models.CharField(max_length=20,choices=CATEGORY_CHOICES,default=MOVIES,)

    genre=models.CharField(max_length=20,choices=GENRE_CHOICES,default=FICTION,)
    publish_date= models.DateField(auto_now_add=True)
    description=models.TextField(max_length=500)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    comments = GenericRelation(Comment)
    
    def __str__(self):
        return self.title + ": " + str(self.videofile)




 
   