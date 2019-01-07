from django.utils.safestring import mark_safe
import markdown
import random
from django.db.models import Count
from django import template

register = template.Library()

from ..models import Stream, Topic

@register.inclusion_tag('index.html')
def get_all_streams():
    all_streams = Stream.objects.all()
    return {'all_streams': all_streams}

@register.inclusion_tag('index.html')
def get_all_topics():
    all_topics = Topic.objects.all()
    return {'all_topics': all_topics}

@register.filter(name='percentage')
def percentage(fraction, population):
    try:
        return "%.2f%%" % ((float(fraction) / float(population)) * 100)
    except ValueError:
        return ''
