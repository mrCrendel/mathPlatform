from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User, Group
from process.models import Stream, Topic, Assignment, AssignmentTopic


class StreamFormCreate(forms.ModelForm):
    # image = ImageField(widget=PictureWidget)
    # description = forzms.CharField(widget=CKEditorWidget(config_name='default'))
    # description_en = forms.CharField(widget=CKEditorWidget(config_name='default'))
    # description = forms.CharField(widget = PagedownWidget(show_preview = False))
    # description_en = forms.CharField(widget = PagedownWidget(show_preview = False))
    class Meta:
        model = Stream
        fields = [
            'title',
            'stream_description',
            'enroll_key',
        ]


class StreamFormUpdate(forms.ModelForm):
    # image = ImageField(widget=PictureWidget)
    # description = forzms.CharField(widget=CKEditorWidget(config_name='default'))
    # description_en = forms.CharField(widget=CKEditorWidget(config_name='default'))
    # description = forms.CharField(widget = PagedownWidget(show_preview = False))
    # description_en = forms.CharField(widget = PagedownWidget(show_preview = False))
    class Meta:
        model = Stream
        fields = [
            'title',
            'users',
            'stream_description',
            'enroll_key',
        ]


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
    answer = forms.CharField(label='')
    class Meta:
        model = Assignment
        fields = []


class AssignmentCreateForm(forms.ModelForm):
    # image = ImageField(widget=PictureWidget)
    # description = forzms.CharField(widget=CKEditorWidget(config_name='default'))
    # description_en = forms.CharField(widget=CKEditorWidget(config_name='default'))
    # description = forms.CharField(widget = PagedownWidget(show_preview = False))
    # description_en = forms.CharField(widget = PagedownWidget(show_preview = False))
    class Meta:
        model = Assignment
        fields = [
            'title',
            'stream',
            'available_from',
            'end_time',
            'available_for_x_minutes',
            'is_exam',
        ]


class AssignmentTopicForm(forms.ModelForm):
    class Meta:
        model = AssignmentTopic
        fields = ['subject', 'topic', 'example_amount', 'points']
        exclude = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.none()


AssignmentTopicFormSet = inlineformset_factory(Assignment, AssignmentTopic, form=AssignmentTopicForm, extra=10)