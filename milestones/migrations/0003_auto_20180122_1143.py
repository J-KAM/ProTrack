# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-22 11:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('milestones', '0002_auto_20180119_1051'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]