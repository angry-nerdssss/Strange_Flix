# Generated by Django 3.0.6 on 2020-11-01 10:58

from django.conf import settings
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('video_title', models.CharField(max_length=100)),
                ('currentTime', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videofile', models.FileField(null=True, upload_to='videos/', verbose_name='')),
                ('poster', models.FileField(null=True, upload_to='images/', verbose_name='')),
                ('captions', models.FileField(null=True, upload_to='captions/', verbose_name='')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=500)),
                ('category', models.CharField(choices=[('movie', 'Movies'), ('show', 'TV Show'), ('series', 'TV Series')], default='movie', max_length=20)),
                ('genre', models.CharField(choices=[('Fiction', 'Fiction'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('Horror', 'Horror'), ('Historical', 'Historical'), ('Romance', 'Romance'), ('Western', 'Western'), ('Fantasy', 'Fantasy'), ('Action', 'Action'), ('Comedy', 'Comedy'), ('Crime', 'Crime'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), ('War', 'War')], default='Fiction', max_length=20)),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('views', models.IntegerField(default=0)),
                ('dislikes', models.ManyToManyField(related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('favourite', models.ManyToManyField(blank=True, related_name='fav_svideos', to=settings.AUTH_USER_MODEL)),
                ('flag', models.ManyToManyField(blank=True, related_name='flag_svideos', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
