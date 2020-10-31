from django import template
from storage_video.models import Video

register = template.Library()

@register.filter
def in_genre(videos, genre):
    return videos.filter(genre=genre)
