# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-01 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0008_auto_20190107_1750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsessionquestions',
            name='points',
            field=models.IntegerField(null=True),
        ),
    ]
