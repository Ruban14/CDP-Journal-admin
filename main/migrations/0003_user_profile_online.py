# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-05 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20190505_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='online',
            field=models.BooleanField(default=True),
        ),
    ]