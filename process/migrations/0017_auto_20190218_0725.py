# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-18 07:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('process', '0016_remove_stream_stream_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='author',
        ),
        migrations.AddField(
            model_name='assignment',
            name='user',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
