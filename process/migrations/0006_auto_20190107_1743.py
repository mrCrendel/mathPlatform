# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-01-07 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0005_auto_20190107_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentsession',
            name='correct_answers',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='assignmentsession',
            name='incorrect_answers',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
    ]
