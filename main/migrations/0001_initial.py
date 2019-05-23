# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-02 17:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Journals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('published_date', models.DateField()),
                ('journal_expiry_date', models.DateField()),
                ('file', models.FileField(max_length=1000, upload_to=main.models.upload_destination)),
                ('Thumbnail', models.ImageField(max_length=1000, upload_to=main.models.upload_destination)),
                ('time_added', models.DateTimeField(auto_now_add=True)),
                ('published_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='published_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='User_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('user_type', models.CharField(choices=[('Admin', 'Admin'), ('User', 'User'), ('Nut', 'Nut')], max_length=25)),
                ('street', models.TextField(blank=True, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('taluk', models.CharField(blank=True, max_length=100, null=True)),
                ('district', models.CharField(blank=True, max_length=100, null=True)),
                ('pincode', models.IntegerField(blank=True, null=True)),
                ('no_of_cocunut_trees', models.IntegerField(blank=True, null=True)),
                ('purpose_of_trees', models.CharField(choices=[('Tender', 'Tender'), ('Neera', 'Neera'), ('Nut', 'Nut')], max_length=25)),
                ('phone_number', models.BigIntegerField()),
                ('need_print', models.BooleanField(default=False)),
            ],
        ),
    ]