from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag()
def mediafile(value):
    """Тег для реобразование пути в полный путь для доступа к медиафайлу."""
    return f'/media/{value}'


@register.filter()
def media_url(value):
    """Фильтр для преобразования пути в полный путь для доступа к медиафайлу."""
    media_root = settings.MEDIA_URL
    return f'{media_root}{value}'

