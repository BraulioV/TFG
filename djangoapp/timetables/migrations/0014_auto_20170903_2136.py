# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-03 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0013_auto_20170903_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='ispractice',
            field=models.CharField(default='F', max_length=2),
        ),
    ]
