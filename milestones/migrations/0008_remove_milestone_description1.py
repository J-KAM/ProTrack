# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-23 11:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('milestones', '0007_milestone_description1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='milestone',
            name='description1',
        ),
    ]
