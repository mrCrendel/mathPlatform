from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.validators import validate_comma_separated_integer_list
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import datetime
from process.include import *
from smart_selects.db_fields import ChainedForeignKey


# Create your models here.
class HomePage(models.Model):
    """ Main page information """
    title = models.CharField(max_length=50, unique=True)
    description = RichTextUploadingField()


class Subject(models.Model):
    title = models.CharField(max_length=50, unique=True)
    subject_code = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('process:subject_detail', kwargs={'slug': self.slug})


class Topic(models.Model):
    title = models.CharField(max_length=50, unique=True)
    subject = models.ForeignKey(Subject,
                                on_delete=models.CASCADE,
                                null=True,
                                blank=False)
    function_code = models.CharField(max_length=50, null=True)
    description = RichTextUploadingField('Question description', default='')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_function_name(self):
        return self.function_code

    def get_absolute_url(self):
        return reverse('process:topic_detail', kwargs={'slug': self.slug})


class Stream(models.Model):
    users = models.ManyToManyField(User, blank=True, related_name='rn_stream')
    title = models.CharField(max_length=50, unique=True)
    stream_description = RichTextUploadingField('Stream description', default='')
    enroll_key = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('process:stream_detail', kwargs={'slug': self.slug})


class Assignment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=50, unique=True)
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    # author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available_from = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    available_for_x_minutes = models.IntegerField(null=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.stream.title + ': ' + self.title


class AssignmentTopic(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='assignment_topic_for')
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    topic = models.ForeignKey(
        Topic,
        # chained_field='subject',
        # chained_model_field='subject',
        # show_all=True,
        # auto_choose=True,
        # sort=True,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    example_amount = models.PositiveIntegerField(default=1)
    points = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.assignment.title + ': ' + self.topic.title


class AssignmentSessionMeneger(models.Manager):
    def create_session(self, user, assignment):
        question = AssignmentTopic.objects.filter(assignment=assignment)
        questions_amount = sum([q.example_amount for q in question])
        assignment_session = self.create(user=user, assignment=assignment, questions_amount=questions_amount)
        return assignment_session


class AssignmentSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    started_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    questions_amount = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)

    is_done = models.BooleanField(default=False)
    current_index = models.IntegerField(default=0)
    objects = AssignmentSessionMeneger()

    def __str__(self):
        return str(self.assignment.title) + ' - ' + str(self.user)


class AssignmentSessionQuestionsMeneger(models.Manager):
    def create_session_question(self, session, assignment,):
        question = AssignmentTopic.objects.filter(assignment=assignment)
        for q in question:
            question_amount = q.example_amount
            print(question_amount)
            question_points = q.points
            topic = Topic.objects.get(title=q.topic)
            topic_code = topic.function_code
            topic_description = topic.description

            while question_amount != 0:
                print(question_amount)
                generated_question = question_creater(topic_code)
                description = topic_description

                if TopicList.is_differential_equation_with(topic_code):
                    description = topic_description.format(generated_question[1], generated_question[2])

                assignment_session_question = self.create(session=session,
                                                          topic=topic,
                                                          question=str(generated_question),
                                                          points=question_points,
                                                          description=description
                                                          )
                question_amount -= 1

        return assignment_session_question


class AssignmentSessionQuestions(models.Model):
    """Automatically  create questions from assignment data for everry session for each user will be differen questoions"""
    QUESTION_TYPES = (
        ('O', 'Open'),
        ('C', 'Closed'),
    )
    session = models.ForeignKey(AssignmentSession,
                                on_delete=models.CASCADE,
                                null=False,
                                blank=False)
    type = models.CharField(max_length=100, choices=QUESTION_TYPES, default='Open')
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        null=False,
        blank=False)
    description = RichTextUploadingField('Question description', default='', null=True, blank=False)
    question = models.CharField(max_length=50)
    question_answer = models.CharField(max_length=100, null=True, blank=False)
    points = models.IntegerField(null=True)
    user_answer = models.CharField(max_length=100, null=True, blank=False)
    is_correct = models.CharField(max_length=100, null=True, blank=False)
    updated = models.DateTimeField(auto_now=True)
    objects = AssignmentSessionQuestionsMeneger()


#create slug for Stream
def create_stream_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Stream.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_stream_slug(instance, new_slug=new_slug)
    return slug


def pre_save_stream_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_stream_slug(instance)


#create slug for Topic
def create_topic_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        lug = new_slug
    qs = Topic.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_topic_slug(instance, new_slug=new_slug)
    return slug


def pre_save_topic_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_topic_slug(instance)


#create dlug for Subject
def create_subject_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Subject.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_subject_slug(instance, new_slug=new_slug)
    return slug


def pre_save_subject_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_subject_slug(instance)


# create slug for Assignment
def create_assignment_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Assignment.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_assignment_slug(instance, new_slug=new_slug)
    return slug

def pre_save_assignment_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_assignment_slug(instance)


#create question from AssingmentTopic model
pre_save.connect(pre_save_stream_post_receiver, sender=Stream)
pre_save.connect(pre_save_topic_post_receiver, sender=Topic)
pre_save.connect(pre_save_subject_post_receiver, sender=Subject)
pre_save.connect(pre_save_assignment_post_receiver, sender=Assignment)
