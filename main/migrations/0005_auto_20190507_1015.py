# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-07 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_user_profile_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_profile',
            name='user_type',
        ),
        migrations.AlterField(
            model_name='user_profile',
            name='pincode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
