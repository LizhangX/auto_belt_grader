# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-05 16:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto_belt_grader', '0002_belt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='belt',
            name='upload',
            field=models.FileField(upload_to='documents/'),
        ),
    ]