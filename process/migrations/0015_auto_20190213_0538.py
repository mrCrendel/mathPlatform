# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-13 05:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0014_auto_20190209_0311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='enroll_key',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
