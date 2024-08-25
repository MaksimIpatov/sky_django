from django import template

register = template.Library()


@register.filter(name="full_media_path")
def full_media(data):
    if data:
        return f'/media/{data}'
    return '#'
