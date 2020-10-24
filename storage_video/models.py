from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
# this model is to save all the details of the uploaded video from the admin
from django.template.defaultfilters import slugify


class Video(models.Model):
    # categories
    MOVIES = 'movie'
    TVSHOW = 'show'
    TVSERIES = 'series'

    # genre
    FICTION = 'Fiction'
    MYSTERY = 'Mystery'
    THRILLER = 'Thriller'
    HORROR = 'Horror'
    HISTORICAL = 'Historical'
    ROMANCE = 'Romance'
    WESTERN = 'Western'
    FANTASY = 'Fantasy'
    ACTION = 'Action'
    COMEDY = 'Comedy'
    CRIME = 'Crime'
    ADVENTURE = 'Adventure'
    ANIMATION = 'Animation'
    WAR = 'War'

    CATEGORY_CHOICES = [

        (MOVIES, 'Movies'),
        (TVSHOW, 'TV Show'),
        (TVSERIES, 'TV Series'),
    ]
    GENRE_CHOICES = [

        (FICTION, 'Fiction'),
        (MYSTERY, 'Mystery'),
        (THRILLER, 'Thriller'),
        (HORROR, 'Horror'),
        (HISTORICAL, 'Historical'),
        (ROMANCE, 'Romance'),
        (WESTERN, 'Western'),
        (FANTASY, 'Fantasy'),
        (ACTION, 'Action'),
        (COMEDY, 'Comedy'),
        (CRIME, 'Crime'),
        (ADVENTURE, 'Adventure'),
        (ANIMATION, 'Animation'),
        (WAR, 'War'),
    ]
    videofile = models.FileField(
        upload_to='videos/', null=True, verbose_name="")
    poster = models.FileField(upload_to='images/', null=True, verbose_name="")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=MOVIES,)
    genre = models.CharField(
        max_length=20, choices=GENRE_CHOICES, default=FICTION,)
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    comments = GenericRelation(Comment)
    likes = models.ManyToManyField(User, related_name='likes')
    """ def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count() """
    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Video, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


""" class Like(models.Model):
    users = models.ManyToManyField(
        User, related_name='requirement_video_likes')
    video = models.OneToOneField(
        Video, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.video.title)[:30]


class Dislike(models.Model):
    users = models.ManyToManyField(
        User, related_name='requirement_video_dis_likes')
    video = models.OneToOneField(
        Video, related_name="dis_likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.video.title)[:30]
 """