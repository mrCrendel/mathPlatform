from django.utils.safestring import mark_safe
import markdown
import random
from django.db.models import Count
from django import template
register = template.Library()
from ..models import *


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
    print('fraction:', fraction, 'population: ', population)
    try:
        return "%.2f%%" % (int((float(population) / float(fraction)) * 100))
    except ValueError:
        return ''


@register.filter(name='count_questions')
def percentage(assignment):
    topics = AssignmentTopic.objects.filter(assignment=assignment)
    sum = 0
    for topic in topics:
        sum += topic.example_amount
    return sum


@register.filter(name='count_user')
def percentage(assignment):
    stream_users = assignment.stream.users.count()
    session_count = AssignmentSession.objects.filter(assignment=assignment).count()
    return '%s/%s' % (stream_users, session_count)