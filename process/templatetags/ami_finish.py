from django import template
from django.shortcuts import render, get_object_or_404
register = template.Library()

from ..models import *


# @register.inclusion_tag('index.html')
# def ami_finish(user, assignment):
#     print('user:', user)
#     print('assignment:', assignment)
#     assignment = assignment
#     print("assignment title: ", assignment)
#     assignment_session = AssignmentSession.objects.get(user=user, assignment=assignment)
#     # assignment_session = get_object_or_404(AssignmentSession, user=user, assignment=assignment)
#     print("assignment session:", assignment_session)
#     index = assignment_session.current_index
#     questions_amount = assignment_session.questions_amount
#     print(index, questions_amount)
#     if index >= questions_amount:
#         print('qq')
#         return {'False': False}
#     else:
#         print('ss')
#         return {'True': True}

@register.filter(name='ami_finish')
def ami_finish(value, user):
    # print(context)
    # u = context['request'].user
    # print(u)
    # user = request.user
    # print('user:', user)
    # print('assignment:', assignment)
    # assignment = assignment
    # print("assignment title: ", assignment)
    assignment_session = AssignmentSession.objects.get(user=user, assignment=value)
    # # assignment_session = get_object_or_404(AssignmentSession, user=user, assignment=assignment)
    # print("assignment session:", assignment_session)
    index = assignment_session.current_index
    questions_amount = assignment_session.questions_amount
    assignment_end = value.end_time
    session_end = assignment_session.started_at + datetime.timedelta(minutes=value.available_for_x_minutes)
    if index >= questions_amount or timezone.now() > assignment_end or timezone.now() > session_end:
        return False
    else:
        return True