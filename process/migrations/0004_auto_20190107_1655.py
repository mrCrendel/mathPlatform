# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-07 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0003_remove_stream_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsession',
            name='correct_answers',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignmentsession',
            name='incorrect_answers',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='assignmentsessionquestions',
            name='is_correct',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
