# Generated by Django 2.2.3 on 2020-10-25 13:45

from django.conf import settings
from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.URLField()),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('movie', 'Movies'), ('show', 'TV Show'), ('series', 'TV Series')], default='movie', max_length=20)),
                ('genre', models.CharField(choices=[('Fiction', 'Fiction'), ('Mystery', 'Mystery'), ('Thriller', 'Thriller'), ('Horror', 'Horror'), ('Historical', 'Historical'), ('Romance', 'Romance'), ('Western', 'Western'), ('Fantasy', 'Fantasy'), ('Action', 'Action'), ('Comedy', 'Comedy'), ('Crime', 'Crime'), ('Adventure', 'Adventure'), ('Animation', 'Animation'), ('War', 'War')], default='Fiction', max_length=20)),
                ('publish_date', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('dislikes', models.ManyToManyField(related_name='ydislikes', to=settings.AUTH_USER_MODEL)),
                ('favourite', models.ManyToManyField(blank=True, related_name='fav_yvideos', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='ylikes', to=settings.AUTH_USER_MODEL)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
    ]
