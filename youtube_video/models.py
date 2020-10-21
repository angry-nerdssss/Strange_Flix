from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


# this model is to save all the details of the uploaded youtube video embed links from the admin
class Item(models.Model):
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
    video = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default=MOVIES,)
    genre = models.CharField(
        max_length=20, choices=GENRE_CHOICES, default=FICTION,)
    publish_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager()
    comments = GenericRelation(Comment)
    favourite = models.ManyToManyField(
        User, related_name="fav_yvideos", blank=True)

    def get_total_likes(self):
        return self.likes.users.count()

    def get_total_dis_likes(self):
        return self.dis_likes.users.count()

    def __str__(self):
        return self.video


class Like(models.Model):
    users = models.ManyToManyField(
        User, related_name='requirement_comment_likes')
    item = models.OneToOneField(
        Item, related_name="likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item.title)[:30]


class Dislike(models.Model):
    users = models.ManyToManyField(
        User, related_name='requirement_comment_dis_likes')
    item = models.OneToOneField(
        Item, related_name="dis_likes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.item.title)[:30]
