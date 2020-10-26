from django.contrib.auth.models import User
from django.db import models
from embed_video.fields import EmbedVideoField
from taggit.managers import TaggableManager
from datetime import date
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.template.defaultfilters import slugify

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
    likes = models.ManyToManyField(User, related_name='ylikes')
    dislikes = models.ManyToManyField(User, related_name='ydislikes')
    favourite = models.ManyToManyField(
        User, related_name="fav_yvideos", blank=True)
    flag = models.ManyToManyField(
        User, related_name="flag_yvideos", blank=True)

    @property
    def total_likes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.likes.count()

    @property
    def total_dislikes(self):
        """
        Likes for the company
        :return: Integer: Likes for the company
        """
        return self.dislikes.count()

    @property
    def total_favourites(self):
        return self.favourite.count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
