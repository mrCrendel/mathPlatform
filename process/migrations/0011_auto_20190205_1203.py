# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-02-05 12:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0010_auto_20190205_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmenttopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='process.Topic'),
        ),
    ]
