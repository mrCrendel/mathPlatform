# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-07 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0004_auto_20190107_1655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentsessionquestions',
            old_name='answer',
            new_name='question_answer',
        ),
        migrations.AddField(
            model_name='assignmentsessionquestions',
            name='user_answer',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
