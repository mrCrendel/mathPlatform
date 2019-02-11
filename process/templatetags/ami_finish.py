from django import template
from django.shortcuts import render, get_object_or_404
register = template.Library()

from ..models import *


@register.filter(name='ami_finish')
def ami_finish(value, user):
    if AssignmentSession.objects.filter(user=user, assignment=value).exists():
        assignment_session = get_object_or_404(AssignmentSession, user=user, assignment=value)
        index = assignment_session.current_index
        questions_amount = assignment_session.questions_amount
        assignment_end = value.end_time
        session_end = assignment_session.started_at + datetime.timedelta(minutes=value.available_for_x_minutes)
        if index >= questions_amount or timezone.now() > assignment_end or timezone.now() > session_end:
            return False
        else:
            return True
    else:
        assignment_session = AssignmentSession.objects.create_session(user, value)
        AssignmentSessionQuestions.objects.create_session_question(assignment_session, value)
        index = assignment_session.current_index
        questions_amount = assignment_session.questions_amount
        assignment_end = value.end_time
        session_end = assignment_session.started_at + datetime.timedelta(minutes=value.available_for_x_minutes)
        if index >= questions_amount or timezone.now() > assignment_end or timezone.now() > session_end:
            return False
        else:
            return True

