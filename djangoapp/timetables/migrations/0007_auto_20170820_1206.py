# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-20 12:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('timetables', '0006_auto_20170820_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='practiceclassroom',
            new_name='classroom',
        ),
    ]
