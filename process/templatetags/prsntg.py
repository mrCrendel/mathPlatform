from django import template
from django.shortcuts import render, get_object_or_404
register = template.Library()

from ..models import *

@register.filter(name='prsntg')
def prsntg():
    return True
