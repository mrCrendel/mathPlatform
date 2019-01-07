from django import forms
from django.contrib.auth.models import User, Group
from process.models import Stream, Topic, Assignment


class StreamEnrollForm(forms.ModelForm):
    """Form that can be used to create a user without the requirement of a password confirmation"""
    enrollment_key = forms.CharField(label='Enrolment key')

    class Meta:
        model = Stream
        fields = []

class StreamUnEnrollForm(forms.ModelForm):
    """Form that can be used to create a user without the requirement of a password confirmation"""

    class Meta:
        model = Stream
        fields = []

        # def user_enrolled(self, form, **kwargs):
        #     stream  = form.instance
        #     enroll_key = form.instance.enroll_key
        #     enrollment_key = form.cleaned_data['enrollment_key']
        #     user = self.request.user
        #
        #     if user in stream.users.all() and enroll_key == enrollment_key:
        #         raise  forms.ValidationError('You are allmostly enrolled')
        #     elif enroll_key == enrollment_key:
        #         raise  forms.ValidationError('You are enrolled to stream')
        #     else:
        #         raise  enrollment_key

class TopicTakeAnswerForm(forms.ModelForm):
    user_answer = forms.CharField(label = 'Enter answer')

    class Meta:
        model = Topic
        fields = []

class AssignmentFormViewForm(forms.ModelForm):
    answer = forms.CharField(label = '')
    class Meta:
        model = Assignment
        fields = []
