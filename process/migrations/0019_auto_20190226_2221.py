# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-26 16:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0018_auto_20190226_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmenttopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.Topic'),
        ),
    ]
